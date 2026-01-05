"""
TradingView Screener Integration (Improved)
Fetches technical indicators from TradingView with proper error handling and validation.

Improvements:
- Removed duplicate function definitions
- Added comprehensive error handling
- Added input validation
- Added retry logic with exponential backoff
- Complete indicator set for trading metrics system
- Proper logging throughout
- Type safety improvements
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional, Tuple
import logging
from time import sleep

logger = logging.getLogger(__name__)


# ==================== CONSTANTS ====================

SUPPORTED_TIMEFRAMES = {
    '5m': '5',
    '15m': '15',
    '1h': '60',
    '4h': '240',
    '1D': '1D',
    '1W': '1W',
    '1M': '1M',
}

# Complete indicator set for trading metrics system
BASE_INDICATORS = [
    'open', 'close', 'volume',
    # Bollinger Bands
    'SMA20', 'BB.upper', 'BB.lower',
    # Additional indicators
    'RSI', 'EMA50',
]

# Extended indicators (verify these column names with TradingView)
EXTENDED_INDICATORS = [
    # Stochastic RSI - VERIFY EXACT COLUMN NAMES
    'Stoch.RSI.K',  # May need adjustment
    'Stoch.RSI.D',  # May need adjustment
    # MACD
    'MACD.macd',
    'MACD.signal',
    'MACD.hist',
    # ADX
    'ADX',
    'ADX.plus',   # May be 'ADX+DI'
    'ADX.minus',  # May be 'ADX-DI'
    # CCI
    'CCI20',
]

DEFAULT_MARKET = 'crypto'
DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_RETRY_DELAY = 2  # seconds


# ==================== HELPER FUNCTIONS ====================

def tf_to_tv_resolution(tf: Optional[str]) -> Optional[str]:
    """
    Map timeframe to TradingView resolution suffix.
    
    Args:
        tf: Timeframe string (e.g., '5m', '1h', '4h', '1D')
    
    Returns:
        TradingView resolution string or None if tf is None/empty
    
    Raises:
        ValueError: If timeframe is not supported
    
    Examples:
        >>> tf_to_tv_resolution('4h')
        '240'
        >>> tf_to_tv_resolution('1D')
        '1D'
        >>> tf_to_tv_resolution(None)
        None
    """
    if not tf:
        return None
    
    if tf not in SUPPORTED_TIMEFRAMES:
        raise ValueError(
            f"Unsupported timeframe: '{tf}'. "
            f"Supported: {list(SUPPORTED_TIMEFRAMES.keys())}"
        )
    
    return SUPPORTED_TIMEFRAMES[tf]


def validate_exchange(exchange: str) -> str:
    """
    Validate and normalize exchange name.
    
    Args:
        exchange: Exchange name (e.g., 'binance', 'kucoin')
    
    Returns:
        Uppercase exchange code
    
    Raises:
        ValueError: If exchange is empty or invalid
    """
    if not exchange or not isinstance(exchange, str):
        raise ValueError("Exchange must be a non-empty string")
    
    return exchange.strip().upper()


def validate_symbols(symbols: Optional[List[str]]) -> Optional[List[str]]:
    """
    Validate symbol list format.
    
    Args:
        symbols: List of ticker symbols (e.g., ['BINANCE:BTCUSDT'])
    
    Returns:
        Validated symbol list or None
    
    Raises:
        ValueError: If symbols format is invalid
    """
    if symbols is None or len(symbols) == 0:
        return None
    
    if not isinstance(symbols, list):
        raise ValueError("Symbols must be a list")
    
    # Validate format (should contain ':')
    for symbol in symbols:
        if not isinstance(symbol, str) or ':' not in symbol:
            raise ValueError(
                f"Invalid symbol format: '{symbol}'. "
                f"Expected format: 'EXCHANGE:PAIR' (e.g., 'BINANCE:BTCUSDT')"
            )
    
    return symbols


def validate_limit(limit: Optional[int]) -> Optional[int]:
    """
    Validate limit parameter.
    
    Args:
        limit: Maximum number of results
    
    Returns:
        Validated limit or None
    
    Raises:
        ValueError: If limit is invalid
    """
    if limit is None:
        return None
    
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError(f"Limit must be a positive integer, got: {limit}")
    
    return limit


def fetch_with_retry(
    query,
    cookies=None,
    max_retries: int = DEFAULT_RETRY_ATTEMPTS,
    base_delay: float = DEFAULT_RETRY_DELAY
) -> Tuple[int, Any]:
    """
    Fetch data from TradingView with exponential backoff retry.
    
    Args:
        query: TradingView Query object
        cookies: Optional requests cookies
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds for exponential backoff
    
    Returns:
        Tuple of (total_count, dataframe)
    
    Raises:
        Exception: If all retry attempts fail
    """
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            logger.debug(f"Fetching data (attempt {attempt + 1}/{max_retries})...")
            total, df = query.get_scanner_data(cookies=cookies)
            logger.info(f"Successfully fetched {total} results")
            return total, df
            
        except Exception as e:
            last_exception = e
            
            if attempt == max_retries - 1:
                logger.error(f"All {max_retries} attempts failed")
                raise
            
            wait_time = base_delay * (2 ** attempt)
            logger.warning(
                f"Attempt {attempt + 1} failed: {e}. "
                f"Retrying in {wait_time}s..."
            )
            sleep(wait_time)
    
    # Should never reach here, but just in case
    raise last_exception or Exception("Unknown error in fetch_with_retry")


def validate_indicator_data(
    indicators: Dict[str, Any],
    symbol: str,
    required_fields: Optional[List[str]] = None
) -> bool:
    """
    Validate that indicator data is complete and valid.
    
    Args:
        indicators: Dictionary of indicator values
        symbol: Symbol name (for logging)
        required_fields: List of required field names
    
    Returns:
        True if valid, False otherwise
    """
    if required_fields is None:
        required_fields = ['open', 'close', 'SMA20', 'BB.upper', 'BB.lower']
    
    # Check for missing fields
    missing = [k for k in required_fields if indicators.get(k) is None]
    if missing:
        logger.warning(f"{symbol}: Missing required indicators: {missing}")
        return False
    
    # Validate price data
    open_price = indicators.get('open')
    close = indicators.get('close')
    
    if open_price is not None and open_price <= 0:
        logger.warning(f"{symbol}: Invalid open price: {open_price}")
        return False
    
    if close is not None and close <= 0:
        logger.warning(f"{symbol}: Invalid close price: {close}")
        return False
    
    # Validate Bollinger Bands
    bb_upper = indicators.get('BB.upper')
    bb_lower = indicators.get('BB.lower')
    
    if bb_upper is not None and bb_lower is not None:
        if bb_upper <= bb_lower:
            logger.warning(
                f"{symbol}: Invalid Bollinger Bands: "
                f"upper={bb_upper} <= lower={bb_lower}"
            )
            return False
    
    return True


# ==================== MAIN FUNCTIONS ====================

def fetch_screener_indicators(
    exchange: str,
    symbols: Optional[List[str]] = None,
    limit: Optional[int] = None,
    timeframe: Optional[str] = None,
    cookies=None,
    include_extended: bool = False,
    validate_data: bool = True,
) -> List[Dict[str, Any]]:
    """
    Fetch indicator columns via TradingView-Screener.
    
    Two modes:
    - Tickers mode: pass symbols => .set_tickers(*symbols)
    - Exchange scan mode: pass symbols=None/[] => filter by exchange
    
    Args:
        exchange: Exchange name (e.g., 'kucoin', 'binance'). Case-insensitive.
        symbols: List of 'EXCHANGE:SYMBOL' tickers. If empty/None, scans by exchange.
        limit: Optional limit of rows to return.
        timeframe: Optional timeframe like '5m', '15m', '1h', '4h', '1D', '1W', '1M'.
        cookies: Optional requests cookies for live data.
        include_extended: Include extended indicators (MACD, StochRSI, ADX, CCI).
        validate_data: Whether to validate indicator data (recommended).
    
    Returns:
        List of dicts: [{'symbol': 'EXCHANGE:PAIR', 'indicators': {...}}]
        Returns empty list on error.
    
    Raises:
        ImportError: If tradingview-screener is not installed.
        ValueError: If parameters are invalid.
    
    Example:
        >>> data = fetch_screener_indicators(
        ...     exchange='binance',
        ...     symbols=['BINANCE:BTCUSDT', 'BINANCE:ETHUSDT'],
        ...     timeframe='4h'
        ... )
        >>> for item in data:
        ...     print(item['symbol'], item['indicators']['close'])
    """
    try:
        from tradingview_screener import Query
        from tradingview_screener.column import Column
    except ImportError as e:
        raise ImportError(
            "tradingview-screener is not installed. "
            "Install with: pip install tradingview-screener"
        ) from e
    
    # Validate inputs
    try:
        exchange_code = validate_exchange(exchange)
        symbols = validate_symbols(symbols)
        limit = validate_limit(limit)
        suffix = tf_to_tv_resolution(timeframe)
    except ValueError as e:
        logger.error(f"Invalid parameters: {e}")
        raise
    
    # Build column list
    cols = BASE_INDICATORS.copy()
    if include_extended:
        cols.extend(EXTENDED_INDICATORS)
    
    # Add timeframe suffix if specified
    if suffix:
        cols = [f"{c}|{suffix}" for c in cols]
        logger.info(f"Using timeframe: {timeframe} (suffix: {suffix})")
    
    # Build query
    q = Query().set_markets(DEFAULT_MARKET).select(*cols)
    
    if symbols:
        # Tickers mode
        logger.info(f"Fetching {len(symbols)} specific symbols")
        q = q.set_tickers(*symbols)
    else:
        # Exchange scan mode
        logger.info(f"Scanning exchange: {exchange_code}")
        q = q.where(Column('exchange') == exchange_code)
    
    if limit:
        q = q.limit(limit)
        logger.info(f"Limiting results to {limit}")
    
    # Fetch data with retry
    try:
        total, df = fetch_with_retry(q, cookies=cookies)
    except Exception as e:
        logger.error(f"Failed to fetch screener data: {e}", exc_info=True)
        return []
    
    # Check if data is empty
    if df is None or df.empty:
        logger.warning(
            f"No data returned for exchange={exchange}, "
            f"symbols={symbols}, timeframe={timeframe}"
        )
        return []
    
    # Normalize column names (remove timeframe suffix)
    if suffix:
        df.rename(
            columns=lambda c: c.split('|')[0] if isinstance(c, str) and '|' in c else c,
            inplace=True
        )
    
    # Process rows
    rows: List[Dict[str, Any]] = []
    skipped = 0
    
    for _, row in df.iterrows():
        symbol = row.get('ticker')
        if not symbol:
            logger.warning("Row missing ticker, skipping")
            continue
        
        # Extract indicators
        indicators = {col: row.get(col) for col in BASE_INDICATORS}
        
        if include_extended:
            for col in EXTENDED_INDICATORS:
                indicators[col] = row.get(col)
        
        # Validate data if requested
        if validate_data:
            if not validate_indicator_data(indicators, symbol):
                skipped += 1
                continue
        
        rows.append({'symbol': symbol, 'indicators': indicators})
    
    if skipped > 0:
        logger.info(f"Skipped {skipped} symbols due to invalid/missing data")
    
    logger.info(f"Successfully processed {len(rows)} symbols")
    return rows


def fetch_screener_multi_changes(
    exchange: str,
    symbols: Optional[List[str]] = None,
    timeframes: Optional[List[str]] = None,
    base_timeframe: str = '4h',
    limit: Optional[int] = None,
    cookies=None,
    validate_data: bool = True,
) -> List[Dict[str, Any]]:
    """
    Fetch multi-timeframe open/close to compute percentage changes per timeframe,
    and include base timeframe indicators needed for trading metrics.
    
    Args:
        exchange: Exchange name (e.g., 'kucoin', 'binance').
        symbols: List of 'EXCHANGE:SYMBOL' tickers. If empty/None, scans by exchange.
        timeframes: List of timeframes to fetch (default: ['15m', '1h', '4h', '1D']).
        base_timeframe: Base timeframe for indicators (default: '4h').
        limit: Optional limit of rows to return.
        cookies: Optional requests cookies for live data.
        validate_data: Whether to validate indicator data.
    
    Returns:
        List of dicts:
        [{
            'symbol': 'KUCOIN:ABCUSDT',
            'changes': {'15m': 1.23, '1h': 2.34, '4h': -0.56, '1D': 3.21},
            'base_indicators': {'open': ..., 'close': ..., 'SMA20': ..., ...}
        }]
    
    Raises:
        ImportError: If tradingview-screener is not installed.
        ValueError: If parameters are invalid.
    
    Example:
        >>> data = fetch_screener_multi_changes(
        ...     exchange='binance',
        ...     timeframes=['1h', '4h', '1D'],
        ...     base_timeframe='4h'
        ... )
    """
    try:
        from tradingview_screener import Query
        from tradingview_screener.column import Column
    except ImportError as e:
        raise ImportError(
            "tradingview-screener is not installed. "
            "Install with: pip install tradingview-screener"
        ) from e
    
    # Validate inputs
    try:
        exchange_code = validate_exchange(exchange)
        symbols = validate_symbols(symbols)
        limit = validate_limit(limit)
    except ValueError as e:
        logger.error(f"Invalid parameters: {e}")
        raise
    
    # Default timeframes
    if not timeframes:
        timeframes = ['15m', '1h', '4h', '1D']
    
    # Build suffix map (filter invalid timeframes)
    suffix_map: Dict[str, str] = {}
    for tf in timeframes:
        try:
            s = tf_to_tv_resolution(tf)
            if s:
                suffix_map[tf] = s
        except ValueError as e:
            logger.warning(f"Skipping invalid timeframe '{tf}': {e}")
    
    # Validate base_timeframe
    try:
        base_suffix = tf_to_tv_resolution(base_timeframe)
        if not base_suffix:
            raise ValueError(f"Invalid base_timeframe: {base_timeframe}")
    except ValueError as e:
        logger.error(f"Invalid base_timeframe: {e}")
        raise
    
    # Fallback if no valid timeframes
    if not suffix_map:
        logger.warning(
            f"No valid timeframes in {timeframes}, "
            f"using base_timeframe only: {base_timeframe}"
        )
        suffix_map = {base_timeframe: base_suffix}
    
    # Build unique column list
    cols_set = set()
    
    # Add open/close for each timeframe
    for tf, s in suffix_map.items():
        cols_set.add(f'open|{s}')
        cols_set.add(f'close|{s}')
    
    # Add base timeframe indicators
    for col in ['SMA20', 'BB.upper', 'BB.lower', 'volume']:
        cols_set.add(f'{col}|{base_suffix}')
    
    cols = list(cols_set)
    logger.info(f"Fetching {len(cols)} columns across {len(suffix_map)} timeframes")
    
    # Build query
    q = Query().set_markets(DEFAULT_MARKET).select(*cols)
    
    if symbols:
        logger.info(f"Fetching {len(symbols)} specific symbols")
        q = q.set_tickers(*symbols)
    else:
        logger.info(f"Scanning exchange: {exchange_code}")
        q = q.where(Column('exchange') == exchange_code)
    
    if limit:
        q = q.limit(limit)
    
    # Fetch data with retry
    try:
        total, df = fetch_with_retry(q, cookies=cookies)
    except Exception as e:
        logger.error(f"Failed to fetch screener data: {e}", exc_info=True)
        return []
    
    # Check if data is empty
    if df is None or df.empty:
        logger.warning(f"No data returned for exchange={exchange}")
        return []
    
    # Process rows
    rows: List[Dict[str, Any]] = []
    skipped = 0
    
    for _, row in df.iterrows():
        symbol = row.get('ticker')
        if not symbol:
            continue
        
        # Calculate percentage changes for each timeframe
        changes: Dict[str, Optional[float]] = {}
        for tf, s in suffix_map.items():
            op = row.get(f'open|{s}')
            cl = row.get(f'close|{s}')
            
            if op is None or op == 0 or cl is None:
                changes[tf] = None
            else:
                changes[tf] = ((cl - op) / op) * 100
        
        # Extract base timeframe indicators
        base_indicators = {
            'open': row.get(f'open|{base_suffix}'),
            'close': row.get(f'close|{base_suffix}'),
            'SMA20': row.get(f'SMA20|{base_suffix}'),
            'BB.upper': row.get(f'BB.upper|{base_suffix}'),
            'BB.lower': row.get(f'BB.lower|{base_suffix}'),
            'volume': row.get(f'volume|{base_suffix}'),
        }
        
        # Validate data if requested
        if validate_data:
            if not validate_indicator_data(base_indicators, symbol):
                skipped += 1
                continue
        
        rows.append({
            'symbol': symbol,
            'changes': changes,
            'base_indicators': base_indicators
        })
    
    if skipped > 0:
        logger.info(f"Skipped {skipped} symbols due to invalid/missing data")
    
    logger.info(f"Successfully processed {len(rows)} symbols")
    return rows


# ==================== INTEGRATION HELPERS ====================

def map_to_trading_metrics_format(indicators: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Map TradingView indicators to trading_metrics.py format.
    
    Note: This requires the extended indicators to be fetched.
    Some indicator names may need adjustment based on TradingView's actual column names.
    
    Args:
        indicators: Raw indicators from fetch_screener_indicators
    
    Returns:
        Formatted indicators for compute_metrics() or None if incomplete
    """
    try:
        # Map to expected format
        formatted = {
            'open': indicators['open'],
            'close': indicators['close'],
            'SMA20': indicators['SMA20'],
            'BB.upper': indicators['BB.upper'],
            'BB.lower': indicators['BB.lower'],
            # Extended indicators (verify column names)
            'StochRSI.K': indicators.get('Stoch.RSI.K'),
            'StochRSI.D': indicators.get('Stoch.RSI.D'),
            'MACD': indicators.get('MACD.macd'),
            'MACD.signal': indicators.get('MACD.signal'),
            'MACD.histogram': indicators.get('MACD.hist'),
            'ADX': indicators.get('ADX'),
            'ADX.plus_di': indicators.get('ADX.plus'),
            'ADX.minus_di': indicators.get('ADX.minus'),
            'CCI': indicators.get('CCI20'),
        }
        
        # Check if all required fields are present
        required = ['open', 'close', 'SMA20', 'BB.upper', 'BB.lower']
        if any(formatted[k] is None for k in required):
            return None
        
        return formatted
        
    except (KeyError, TypeError) as e:
        logger.error(f"Error mapping indicators: {e}")
        return None
