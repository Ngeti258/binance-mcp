#!/usr/bin/env python3
"""
Automated Major Cryptocurrencies Analysis - FULLY AUTOMATED
Analyzes top 15 major cryptocurrencies with technical indicators
Generates markdown reports with trading opportunities

NO USER INPUT REQUIRED - Runs completely automatically
Optimized for Nairobi/Kenya timezone (EAT - UTC+3)
"""

import sys
import os
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add project to path
sys.path.append(str(Path(__file__).parent))

# Try to import optional dependencies
try:
    from paper_trading_db import PaperTradingDB
    HAS_PAPER_TRADING = True
except ImportError:
    HAS_PAPER_TRADING = False
    logger.warning("paper_trading_db not available - paper trading features disabled")

try:
    from tradingview_screener import Query
    HAS_TRADINGVIEW = True
except ImportError:
    HAS_TRADINGVIEW = False
    logger.warning("tradingview-screener not available - using Binance data only")

# Try to import pytz, fall back to manual offset
try:
    import pytz
    EAT = pytz.timezone('Africa/Nairobi')
    def get_nairobi_time():
        return datetime.now(EAT)
except ImportError:
    from datetime import timezone, timedelta
    EAT_OFFSET = timezone(timedelta(hours=3))
    def get_nairobi_time():
        return datetime.now(EAT_OFFSET)

# ==================== CONFIGURATION ====================

# Major cryptocurrencies to analyze
MAJOR_SYMBOLS = [
    'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT',
    'ADAUSDT', 'AVAXUSDT', 'DOTUSDT', 'MATICUSDT', 'LINKUSDT',
    'UNIUSDT', 'ATOMUSDT', 'LTCUSDT', 'TRXUSDT', 'DOGEUSDT'
]

# Binance API endpoint
BINANCE_API_BASE = "https://api.binance.com/api/v3"

# Default USD to KES rate
DEFAULT_USD_TO_KES = 129.50

# TradingView indicators to fetch
TV_INDICATORS = [
    'close', 'open', 'high', 'low', 'volume',
    'RSI', 'RSI[1]',
    'MACD.macd', 'MACD.signal',
    'EMA20', 'EMA50', 'EMA200',
    'SMA20', 'BB.upper', 'BB.lower',
    'Stoch.K', 'Stoch.D',
    'ADX', 'CCI20', 'Mom',
    'Recommend.All', 'Recommend.MA', 'Recommend.Other'
]

# ==================== API FUNCTIONS ====================

def get_usd_to_kes_rate() -> float:
    """Get current USD to KES exchange rate"""
    try:
        response = requests.get(
            "https://api.exchangerate-api.com/v4/latest/USD",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('rates', {}).get('KES', DEFAULT_USD_TO_KES)
    except Exception as e:
        logger.warning(f"Failed to get exchange rate: {e}")
    return DEFAULT_USD_TO_KES

def get_binance_prices(symbols: List[str]) -> Dict[str, float]:
    """Fetch current prices from Binance"""
    prices = {}
    try:
        response = requests.get(f"{BINANCE_API_BASE}/ticker/price", timeout=10)
        response.raise_for_status()
        all_prices = response.json()
        price_lookup = {item['symbol']: float(item['price']) for item in all_prices}

        for symbol in symbols:
            if symbol in price_lookup:
                prices[symbol] = price_lookup[symbol]
    except Exception as e:
        logger.error(f"Failed to fetch Binance prices: {e}")
    return prices

def get_binance_24h_stats(symbols: List[str]) -> Dict[str, Dict]:
    """Fetch 24h statistics from Binance"""
    stats = {}
    try:
        response = requests.get(f"{BINANCE_API_BASE}/ticker/24hr", timeout=15)
        response.raise_for_status()
        all_stats = response.json()
        stats_lookup = {item['symbol']: item for item in all_stats}

        for symbol in symbols:
            if symbol in stats_lookup:
                item = stats_lookup[symbol]
                stats[symbol] = {
                    'price': float(item['lastPrice']),
                    'change_24h': float(item['priceChangePercent']),
                    'high_24h': float(item['highPrice']),
                    'low_24h': float(item['lowPrice']),
                    'volume_24h': float(item['volume']),
                    'quote_volume_24h': float(item['quoteVolume'])
                }
    except Exception as e:
        logger.error(f"Failed to fetch Binance 24h stats: {e}")
    return stats

def get_tradingview_indicators(symbols: List[str], timeframe: str = '1h') -> Dict[str, Dict]:
    """Fetch technical indicators from TradingView"""
    if not HAS_TRADINGVIEW:
        return {}

    indicators = {}

    # Map timeframe to TradingView format
    tf_map = {'1h': '60', '4h': '240', '1d': '1D', '1w': '1W'}
    tv_tf = tf_map.get(timeframe, '60')

    try:
        # Build tickers list
        tickers = [f"BINANCE:{symbol}" for symbol in symbols]

        # Build columns with timeframe suffix
        columns = [f"{ind}|{tv_tf}" for ind in TV_INDICATORS]

        # Create query
        query = Query().set_markets('crypto').select(*columns).set_tickers(*tickers)

        # Fetch data
        count, df = query.get_scanner_data()

        if df is not None and not df.empty:
            for _, row in df.iterrows():
                ticker = row.get('ticker', '')
                symbol = ticker.replace('BINANCE:', '')

                if symbol in symbols:
                    indicators[symbol] = {}
                    for ind in TV_INDICATORS:
                        col_name = f"{ind}|{tv_tf}"
                        indicators[symbol][ind] = row.get(col_name)

    except Exception as e:
        logger.error(f"Failed to fetch TradingView indicators: {e}")

    return indicators

# ==================== ANALYSIS FUNCTIONS ====================

def get_signal_from_recommendation(rec_value: float) -> str:
    """Convert TradingView recommendation value to signal"""
    if rec_value is None:
        return "NEUTRAL"
    if rec_value >= 0.5:
        return "STRONG_BUY"
    elif rec_value >= 0.1:
        return "BUY"
    elif rec_value <= -0.5:
        return "STRONG_SELL"
    elif rec_value <= -0.1:
        return "SELL"
    return "NEUTRAL"

def get_rsi_signal(rsi: float) -> str:
    """Analyze RSI value"""
    if rsi is None:
        return "NEUTRAL"
    if rsi > 70:
        return "OVERBOUGHT"
    elif rsi < 30:
        return "OVERSOLD"
    elif rsi > 60:
        return "BULLISH"
    elif rsi < 40:
        return "BEARISH"
    return "NEUTRAL"

def analyze_coin(symbol: str, stats: Dict, tv_data: Dict, usd_to_kes: float) -> Dict:
    """Analyze a single coin"""
    analysis = {
        'symbol': symbol,
        'price_usd': stats.get('price', 0),
        'price_kes': stats.get('price', 0) * usd_to_kes,
        'change_24h': stats.get('change_24h', 0),
        'volume_24h_usd': stats.get('quote_volume_24h', 0),
        'high_24h': stats.get('high_24h', 0),
        'low_24h': stats.get('low_24h', 0),
    }

    # Add TradingView indicators if available
    if tv_data:
        analysis['rsi'] = tv_data.get('RSI')
        analysis['rsi_signal'] = get_rsi_signal(tv_data.get('RSI'))
        analysis['macd'] = tv_data.get('MACD.macd')
        analysis['macd_signal'] = tv_data.get('MACD.signal')
        analysis['ema20'] = tv_data.get('EMA20')
        analysis['ema50'] = tv_data.get('EMA50')
        analysis['ema200'] = tv_data.get('EMA200')
        analysis['bb_upper'] = tv_data.get('BB.upper')
        analysis['bb_lower'] = tv_data.get('BB.lower')
        analysis['adx'] = tv_data.get('ADX')
        analysis['cci'] = tv_data.get('CCI20')

        # Overall signals
        rec_all = tv_data.get('Recommend.All')
        rec_ma = tv_data.get('Recommend.MA')
        rec_other = tv_data.get('Recommend.Other')

        analysis['signal_overall'] = get_signal_from_recommendation(rec_all)
        analysis['signal_ma'] = get_signal_from_recommendation(rec_ma)
        analysis['signal_oscillators'] = get_signal_from_recommendation(rec_other)

        # Trend analysis
        price = stats.get('price', 0)
        ema20 = tv_data.get('EMA20')
        ema50 = tv_data.get('EMA50')
        ema200 = tv_data.get('EMA200')

        if price and ema20 and ema50:
            if price > ema20 > ema50:
                analysis['trend'] = "UPTREND"
            elif price < ema20 < ema50:
                analysis['trend'] = "DOWNTREND"
            else:
                analysis['trend'] = "SIDEWAYS"
        else:
            analysis['trend'] = "UNKNOWN"
    else:
        # Default values if no TV data
        analysis['signal_overall'] = "NEUTRAL"
        analysis['signal_ma'] = "NEUTRAL"
        analysis['signal_oscillators'] = "NEUTRAL"
        analysis['trend'] = "UNKNOWN"

    return analysis

def generate_trading_opportunities(analyses: List[Dict]) -> List[Dict]:
    """Generate trading opportunities from analysis"""
    opportunities = []

    for analysis in analyses:
        signal = analysis.get('signal_overall', 'NEUTRAL')
        trend = analysis.get('trend', 'UNKNOWN')
        rsi = analysis.get('rsi')
        change_24h = analysis.get('change_24h', 0)

        # Skip neutral signals
        if signal == 'NEUTRAL':
            continue

        # Determine trade setup
        if signal in ['STRONG_BUY', 'BUY']:
            side = 'LONG'
            if rsi and rsi < 35:
                confidence = 'HIGH'
                reason = "Oversold bounce opportunity"
            elif trend == 'UPTREND':
                confidence = 'MEDIUM-HIGH'
                reason = "Trend continuation"
            else:
                confidence = 'MEDIUM'
                reason = "Bullish signals"

        elif signal in ['STRONG_SELL', 'SELL']:
            side = 'SHORT'
            if rsi and rsi > 65:
                confidence = 'HIGH'
                reason = "Overbought reversal"
            elif trend == 'DOWNTREND':
                confidence = 'MEDIUM-HIGH'
                reason = "Trend continuation"
            else:
                confidence = 'MEDIUM'
                reason = "Bearish signals"
        else:
            continue

        price = analysis['price_usd']

        # Calculate levels
        if side == 'LONG':
            stop_loss = price * 0.98  # 2% below
            target1 = price * 1.02  # 2% above
            target2 = price * 1.04  # 4% above
        else:
            stop_loss = price * 1.02  # 2% above
            target1 = price * 0.98  # 2% below
            target2 = price * 0.96  # 4% below

        opportunities.append({
            'symbol': analysis['symbol'],
            'side': side,
            'signal': signal,
            'confidence': confidence,
            'reason': reason,
            'entry_price': price,
            'stop_loss': stop_loss,
            'target1': target1,
            'target2': target2,
            'rsi': rsi,
            'trend': trend,
            'change_24h': change_24h
        })

    # Sort by confidence
    confidence_order = {'HIGH': 0, 'MEDIUM-HIGH': 1, 'MEDIUM': 2, 'MEDIUM-LOW': 3, 'LOW': 4}
    opportunities.sort(key=lambda x: confidence_order.get(x['confidence'], 5))

    return opportunities

# ==================== REPORT GENERATION ====================

def generate_markdown_report(
    analyses: List[Dict],
    opportunities: List[Dict],
    usd_to_kes: float,
    timestamp: datetime
) -> str:
    """Generate markdown report"""

    report = []
    report.append(f"# Major Cryptocurrencies Analysis")
    report.append(f"")
    report.append(f"**Generated:** {timestamp.strftime('%Y-%m-%d %H:%M:%S')} EAT (Nairobi)")
    report.append(f"**USD/KES Rate:** {usd_to_kes:.2f}")
    report.append(f"**Coins Analyzed:** {len(analyses)}")
    report.append(f"")
    report.append(f"---")
    report.append(f"")

    # Market Summary
    report.append(f"## Market Summary")
    report.append(f"")

    bullish = sum(1 for a in analyses if a.get('change_24h', 0) > 0)
    bearish = len(analyses) - bullish
    avg_change = sum(a.get('change_24h', 0) for a in analyses) / len(analyses) if analyses else 0

    report.append(f"- **Bullish:** {bullish} coins ({bullish/len(analyses)*100:.0f}%)")
    report.append(f"- **Bearish:** {bearish} coins ({bearish/len(analyses)*100:.0f}%)")
    report.append(f"- **Average 24h Change:** {avg_change:+.2f}%")
    report.append(f"")

    # Price Table
    report.append(f"## Current Prices")
    report.append(f"")
    report.append(f"| Coin | Price (USD) | Price (KES) | 24h Change | Signal | Trend |")
    report.append(f"|------|-------------|-------------|------------|--------|-------|")

    for a in sorted(analyses, key=lambda x: x.get('quote_volume_24h', 0) if x.get('quote_volume_24h') else x.get('volume_24h_usd', 0), reverse=True):
        symbol = a['symbol'].replace('USDT', '')
        price_usd = a['price_usd']
        price_kes = a['price_kes']
        change = a.get('change_24h', 0)
        signal = a.get('signal_overall', 'N/A')
        trend = a.get('trend', 'N/A')

        change_str = f"+{change:.2f}%" if change >= 0 else f"{change:.2f}%"

        if price_usd >= 1000:
            price_usd_str = f"${price_usd:,.0f}"
            price_kes_str = f"KSh {price_kes:,.0f}"
        elif price_usd >= 1:
            price_usd_str = f"${price_usd:,.2f}"
            price_kes_str = f"KSh {price_kes:,.2f}"
        else:
            price_usd_str = f"${price_usd:.4f}"
            price_kes_str = f"KSh {price_kes:.4f}"

        report.append(f"| {symbol} | {price_usd_str} | {price_kes_str} | {change_str} | {signal} | {trend} |")

    report.append(f"")

    # Trading Opportunities
    if opportunities:
        report.append(f"## Trading Opportunities")
        report.append(f"")
        report.append(f"Found **{len(opportunities)}** potential setups:")
        report.append(f"")

        for opp in opportunities:
            symbol = opp['symbol'].replace('USDT', '')
            side = opp['side']
            confidence = opp['confidence']
            reason = opp['reason']
            entry = opp['entry_price']
            sl = opp['stop_loss']
            tp1 = opp['target1']
            tp2 = opp['target2']

            emoji = "🟢" if side == "LONG" else "🔴"

            report.append(f"### {emoji} {symbol} - {side}")
            report.append(f"")
            report.append(f"- **Signal:** {opp['signal']}")
            report.append(f"- **Confidence:** {confidence}")
            report.append(f"- **Reason:** {reason}")
            report.append(f"- **Entry:** ${entry:,.2f}")
            report.append(f"- **Stop Loss:** ${sl:,.2f} ({((sl-entry)/entry)*100:+.1f}%)")
            report.append(f"- **Target 1:** ${tp1:,.2f} ({((tp1-entry)/entry)*100:+.1f}%)")
            report.append(f"- **Target 2:** ${tp2:,.2f} ({((tp2-entry)/entry)*100:+.1f}%)")
            if opp.get('rsi'):
                report.append(f"- **RSI:** {opp['rsi']:.1f}")
            report.append(f"")
    else:
        report.append(f"## Trading Opportunities")
        report.append(f"")
        report.append(f"No strong trading opportunities identified at this time.")
        report.append(f"")

    # Technical Analysis Details
    report.append(f"## Technical Analysis Details")
    report.append(f"")

    for a in analyses[:5]:  # Top 5 by volume
        symbol = a['symbol'].replace('USDT', '')
        report.append(f"### {symbol}")
        report.append(f"")
        report.append(f"| Indicator | Value | Signal |")
        report.append(f"|-----------|-------|--------|")

        if a.get('rsi'):
            report.append(f"| RSI (14) | {a['rsi']:.1f} | {a.get('rsi_signal', 'N/A')} |")
        if a.get('macd') is not None:
            macd_status = "Bullish" if a['macd'] > (a.get('macd_signal') or 0) else "Bearish"
            report.append(f"| MACD | {a['macd']:.4f} | {macd_status} |")
        if a.get('adx'):
            adx_status = "Strong" if a['adx'] > 25 else "Weak"
            report.append(f"| ADX | {a['adx']:.1f} | {adx_status} |")

        report.append(f"| Trend | {a.get('trend', 'N/A')} | - |")
        report.append(f"| Overall Signal | {a.get('signal_overall', 'N/A')} | - |")
        report.append(f"")

    # Footer
    report.append(f"---")
    report.append(f"")
    report.append(f"*Analysis generated automatically by Nairobi Trading System*")
    report.append(f"*Next analysis scheduled in 4 hours*")

    return "\n".join(report)

# ==================== MAIN FUNCTION ====================

def run_automated_analysis():
    """
    Main automated analysis function
    NO USER INPUT REQUIRED
    """
    timestamp = get_nairobi_time()

    print("\n" + "=" * 80)
    print("AUTOMATED MAJOR CRYPTOCURRENCIES ANALYSIS")
    print(f"Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')} EAT")
    print("=" * 80)

    # Get exchange rate
    print("\nFetching USD/KES exchange rate...")
    usd_to_kes = get_usd_to_kes_rate()
    print(f"USD/KES Rate: {usd_to_kes:.2f}")

    # Get Binance 24h stats
    print(f"\nFetching Binance data for {len(MAJOR_SYMBOLS)} symbols...")
    binance_stats = get_binance_24h_stats(MAJOR_SYMBOLS)
    print(f"Received data for {len(binance_stats)} symbols")

    # Get TradingView indicators
    if HAS_TRADINGVIEW:
        print("\nFetching TradingView indicators (1h timeframe)...")
        tv_indicators_1h = get_tradingview_indicators(MAJOR_SYMBOLS, '1h')
        print(f"Received TV data for {len(tv_indicators_1h)} symbols")
    else:
        print("\nSkipping TradingView (not installed)")
        tv_indicators_1h = {}

    # Analyze each coin
    print("\nAnalyzing coins...")
    analyses = []
    for symbol in MAJOR_SYMBOLS:
        if symbol in binance_stats:
            tv_data = tv_indicators_1h.get(symbol, {})
            analysis = analyze_coin(symbol, binance_stats[symbol], tv_data, usd_to_kes)
            analyses.append(analysis)

    print(f"Analyzed {len(analyses)} coins")

    # Generate trading opportunities
    print("\nIdentifying trading opportunities...")
    opportunities = generate_trading_opportunities(analyses)
    print(f"Found {len(opportunities)} potential setups")

    # Generate report
    print("\nGenerating markdown report...")
    report = generate_markdown_report(analyses, opportunities, usd_to_kes, timestamp)

    # Save report
    report_filename = f"majors-analysis-{timestamp.strftime('%Y-%m-%d-%H-%M')}.md"
    report_path = Path(__file__).parent / report_filename

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nReport saved: {report_filename}")

    # Log execution
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "analysis_runs.log"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] Analysis completed\n")
        f.write(f"  - Coins analyzed: {len(analyses)}\n")
        f.write(f"  - Opportunities found: {len(opportunities)}\n")
        f.write(f"  - Report: {report_filename}\n")

    # Summary
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

    # Quick market summary
    bullish = sum(1 for a in analyses if a.get('change_24h', 0) > 0)
    bearish = len(analyses) - bullish

    print(f"\nMarket: {bullish} bullish, {bearish} bearish")

    if opportunities:
        print(f"\nTop Opportunities:")
        for opp in opportunities[:3]:
            symbol = opp['symbol'].replace('USDT', '')
            print(f"  {opp['side']} {symbol} @ ${opp['entry_price']:,.2f} ({opp['confidence']})")

    print(f"\nNext analysis: 4 hours")
    print("=" * 80 + "\n")

    return {
        'analyses': analyses,
        'opportunities': opportunities,
        'report_path': str(report_path)
    }

if __name__ == "__main__":
    """
    Run automated analysis
    No user input required
    """
    run_automated_analysis()
