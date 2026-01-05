"""
TradingView Screener Integration Module
-------------------------------------
Fetches technical indicators from TradingView's screener API for cryptocurrency trading.
Supports single and multi-timeframe analysis with robust error handling and validation.
"""

import logging
import time
from typing import List, Dict, Any, Optional, Union
from trading_metrics import compute_metrics
from trading_utils import get_trading_recommendation

# Configure logging
logger = logging.getLogger(__name__)

def _tf_to_tv_resolution(tf: Optional[str]) -> Optional[str]:
    """
    Map our timeframe to TradingView resolution suffix used in columns.
    Returns None if no mapping (means: no suffix).
    
    Args:
        tf: Timeframe string (e.g., '5m', '1h', '1D')
        
    Returns:
        TradingView resolution string or None
        
    Raises:
        ValueError: If timeframe is not supported
    """
    if not tf:
        return None
        
    mapping = {
        '1m': '1',
        '5m': '5',
        '15m': '15',
        '1h': '60',
        '4h': '240',
        '1D': '1D',
        '1W': '1W',
        '1M': '1M',
    }
    
    if tf not in mapping:
        # Log warning but return None to allow fallback/custom handling if needed
        logger.warning(f"Unsupported timeframe: {tf}. Supported: {list(mapping.keys())}")
        return None
        
    return mapping.get(tf)

def validate_indicator_data(indicators: Dict[str, Any], symbol: str) -> bool:
    """
    Validate that indicator data is complete and valid.
    
    Args:
        indicators: Dictionary of indicator values
        symbol: Symbol name for logging
        
    Returns:
        True if valid, False otherwise
    """
    # Required fields for basic analysis
    required = ['open', 'close', 'SMA20', 'BB.upper', 'BB.lower']
    
    # Check for missing values
    missing = [k for k in required if indicators.get(k) is None]
    if missing:
        logger.warning(f"{symbol}: Missing required indicators: {missing}")
        return False
    
    # Validate prices
    try:
        if indicators.get('open', 0) <= 0 or indicators.get('close', 0) <= 0:
            logger.warning(f"{symbol}: Invalid prices (<= 0)")
            return False
            
        # Validate Bollinger Bands
        bb_upper = indicators.get('BB.upper')
        bb_lower = indicators.get('BB.lower')
        if bb_upper is not None and bb_lower is not None and bb_upper <= bb_lower:
            logger.warning(f"{symbol}: Invalid Bollinger Bands (upper <= lower)")
            return False
            
    except (TypeError, ValueError) as e:
        logger.warning(f"{symbol}: Validation error: {e}")
        return False
    
    return True

def fetch_screener_indicators(
    exchange: str,
    symbols: Optional[List[str]] = None,
    limit: Optional[int] = None,
    timeframe: Optional[str] = None,
    cookies=None,
    max_retries: int = 3
) -> List[Dict[str, Any]]:
    """
    Fetch indicator columns via TradingView-Screener.
    
    Args:
        exchange: e.g. 'kucoin' or 'binance'. Case-insensitive.
        symbols: list of 'EXCHANGE:SYMBOL' tickers. If empty/None, scans by exchange.
        limit: optional limit of rows to return.
        timeframe: optional timeframe like '5m', '15m', '1h', '4h', '1D', '1W', '1M'.
        cookies: optional requests cookies for live data.
        max_retries: number of retries for API calls.

    Returns: 
        List[{ 'symbol': 'EXCHANGE:PAIR', 'indicators': {...} }]
    """
    try:
        from tradingview_screener import Query
        from tradingview_screener.column import Column
    except ImportError as e:
        logger.error("tradingview-screener not installed. Run: pip install tradingview-screener")
        return []

    market = 'crypto'
    
    # Complete indicator set required for trading_metrics.py
    # Note: Column names must match TradingView's internal names
    base_cols = [
        'open', 'close', 'volume',
        # Bollinger Bands
        'SMA20', 'BB.upper', 'BB.lower',
        # Stochastic RSI
        'Stoch.RSI.K', 'Stoch.RSI.D',
        # MACD
        'MACD.macd', 'MACD.signal', 'MACD.hist',
        # ADX
        'ADX', 'ADX+DI', 'ADX-DI',
        # CCI
        'CCI20',
        # Optional but useful
        'RSI', 'EMA50'
    ]

    suffix = _tf_to_tv_resolution(timeframe)
    cols = [f"{c}|{suffix}" if suffix else c for c in base_cols]

    q = Query().set_markets(market).select(*cols)

    exchange_code = (exchange or '').upper()

    if symbols:
        # Tickers mode
        q = q.set_tickers(*symbols)
    else:
        # Exchange scan mode
        if exchange_code:
            q = q.where(Column('exchange') == exchange_code)

    if limit:
        q = q.limit(int(limit))

    # Retry logic
    df = None
    for attempt in range(max_retries):
        try:
            total, df = q.get_scanner_data(cookies=cookies)
            break
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed to fetch screener data after {max_retries} attempts: {e}")
                return []
            wait_time = 2 ** attempt
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)

    rows: List[Dict[str, Any]] = []
    if df is None or df.empty:
        logger.warning(f"No data returned for exchange={exchange}, symbols={symbols}")
        return rows

    # Normalize column names
    # If we used timeframe suffix (e.g., 'close|240'), normalize back to base (e.g., 'close')
    df.rename(columns=lambda c: c.split('|')[0] if isinstance(c, str) else c, inplace=True)

    for _, row in df.iterrows():
        symbol = row.get('ticker')
        
        # Map TradingView columns to our internal names
        indicators = {
            'open': row.get('open'),
            'close': row.get('close'),
            'volume': row.get('volume'),
            'SMA20': row.get('SMA20'),
            'BB.upper': row.get('BB.upper'),
            'BB.lower': row.get('BB.lower'),
            'StochRSI.K': row.get('Stoch.RSI.K'),
            'StochRSI.D': row.get('Stoch.RSI.D'),
            'MACD': row.get('MACD.macd'),
            'MACD.signal': row.get('MACD.signal'),
            'MACD.histogram': row.get('MACD.hist'),
            'ADX': row.get('ADX'),
            'ADX.plus_di': row.get('ADX+DI'),
            'ADX.minus_di': row.get('ADX-DI'),
            'CCI': row.get('CCI20'),
            'RSI': row.get('RSI'),
            'EMA50': row.get('EMA50'),
        }

        rows.append({'symbol': symbol, 'indicators': indicators})

    return rows

def fetch_screener_multi_changes(
    exchange: str,
    symbols: Optional[List[str]] = None,
    timeframes: Optional[List[str]] = None,
    base_timeframe: str = '4h',
    limit: Optional[int] = None,
    cookies=None,
) -> List[Dict[str, Any]]:
    """
    Fetch multi-timeframe open/close to compute percentage changes per timeframe,
    and also include base timeframe indicators needed for BB metrics.

    Returns rows like:
      {
        'symbol': 'KUCOIN:ABCUSDT',
        'changes': { '15m': 1.23, '1h': 2.34, '4h': -0.56, '1D': 3.21 },
        'base_indicators': { 'open': ..., 'close': ..., 'SMA20': ..., 'BB.upper': ..., 'BB.lower': ..., 'volume': ... }
      }
    """
    try:
        from tradingview_screener import Query
        from tradingview_screener.column import Column
    except ImportError:
        logger.error("tradingview-screener not installed")
        return []

    # Default timeframe set
    if not timeframes:
        timeframes = ['15m', '1h', '4h', '1D']

    # Build suffix map and filter invalid tfs
    suffix_map: Dict[str, str] = {}
    for tf in timeframes:
        s = _tf_to_tv_resolution(tf)
        if s:
            suffix_map[tf] = s
            
    if not suffix_map:
        logger.warning(f"No valid timeframes in {timeframes}, using base: {base_timeframe}")
        bs = _tf_to_tv_resolution(base_timeframe)
        if bs:
            suffix_map = {base_timeframe: bs}
        else:
            # Fallback to 4h if base is also invalid
            suffix_map = {base_timeframe: '240'}

    base_suffix = _tf_to_tv_resolution(base_timeframe) or '240'

    # Build columns using set to avoid duplicates
    cols_set = set()
    
    # Add change columns
    for tf, s in suffix_map.items():
        cols_set.add(f'open|{s}')
        cols_set.add(f'close|{s}')
        
    # Add base indicators
    base_cols = [
        f'open|{base_suffix}', f'close|{base_suffix}', 
        f'SMA20|{base_suffix}', f'BB.upper|{base_suffix}', f'BB.lower|{base_suffix}', 
        f'volume|{base_suffix}'
    ]
    cols_set.update(base_cols)
    
    cols = list(cols_set)

    q = Query().set_markets('crypto').select(*cols)

    exchange_code = (exchange or '').upper()
    if symbols:
        q = q.set_tickers(*symbols)
    else:
        if exchange_code:
            q = q.where(Column('exchange') == exchange_code)
            
    if limit:
        q = q.limit(int(limit))

    try:
        total, df = q.get_scanner_data(cookies=cookies)
    except Exception as e:
        logger.error(f"Failed to fetch multi-change data: {e}")
        return []
        
    rows: List[Dict[str, Any]] = []
    if df is None or df.empty:
        return rows

    # Iterate rows and compute changes per tf; prepare base indicators
    for _, row in df.iterrows():
        symbol = row.get('ticker')
        changes: Dict[str, Optional[float]] = {}
        
        for tf, s in suffix_map.items():
            op = row.get(f'open|{s}')
            cl = row.get(f'close|{s}')
            
            if op is None or op == 0 or cl is None:
                changes[tf] = None
            else:
                changes[tf] = ((cl - op) / op) * 100

        # Note: We keep the raw column names here as we didn't rename them
        base_indicators = {
            'open': row.get(f'open|{base_suffix}'),
            'close': row.get(f'close|{base_suffix}'),
            'SMA20': row.get(f'SMA20|{base_suffix}'),
            'BB.upper': row.get(f'BB.upper|{base_suffix}'),
            'BB.lower': row.get(f'BB.lower|{base_suffix}'),
            'volume': row.get(f'volume|{base_suffix}'),
        }

        rows.append({'symbol': symbol, 'changes': changes, 'base_indicators': base_indicators})

    return rows

def get_trading_signals(exchange: str, symbols: List[str], timeframe: str = '4h') -> List[Dict[str, Any]]:
    """
    Fetch indicators and compute trading signals for a list of symbols.
    
    Args:
        exchange: Exchange name (e.g., 'BINANCE')
        symbols: List of symbols (e.g., ['BINANCE:BTCUSDT'])
        timeframe: Timeframe to analyze
        
    Returns:
        List of results with metrics and signals
    """
    # Fetch data
    data = fetch_screener_indicators(
        exchange=exchange,
        symbols=symbols,
        timeframe=timeframe
    )
    
    results = []
    for item in data:
        symbol = item['symbol']
        indicators = item['indicators']
        
        # Validate data
        if not validate_indicator_data(indicators, symbol):
            continue
        
        # Compute metrics
        metrics = compute_metrics(indicators)
        if metrics:
            results.append({
                'symbol': symbol,
                'metrics': metrics,
                'signal': metrics['composite']['signal'],
                'rating': metrics['composite']['rating'],
                'recommendation': get_trading_recommendation(metrics)
            })
    
    return results
