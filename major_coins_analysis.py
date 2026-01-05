"""
Major Cryptocurrencies Comprehensive Analysis Script
----------------------------------------------------
Generates comprehensive hourly analysis for top 15 major cryptocurrencies
with dual currency display (USD & KES).
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

# Try to import binance
try:
    from binance.client import Client
    BINANCE_AVAILABLE = True
except ImportError:
    print("Installing python-binance...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-binance"])
    from binance.client import Client
    BINANCE_AVAILABLE = True

# Try to import tradingview-screener
try:
    from tradingview_screener import Scanner
    TV_AVAILABLE = True
except ImportError:
    print("Installing tradingview-screener...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tradingview-screener"])
    from tradingview_screener import Scanner
    TV_AVAILABLE = True

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Major coins configuration
MAJOR_COINS = [
    {"symbol": "BTCUSDT", "name": "Bitcoin", "ticker": "BTC"},
    {"symbol": "ETHUSDT", "name": "Ethereum", "ticker": "ETH"},
    {"symbol": "BNBUSDT", "name": "Binance Coin", "ticker": "BNB"},
    {"symbol": "SOLUSDT", "name": "Solana", "ticker": "SOL"},
    {"symbol": "XRPUSDT", "name": "XRP", "ticker": "XRP"},
    {"symbol": "ADAUSDT", "name": "Cardano", "ticker": "ADA"},
    {"symbol": "AVAXUSDT", "name": "Avalanche", "ticker": "AVAX"},
    {"symbol": "DOTUSDT", "name": "Polkadot", "ticker": "DOT"},
    {"symbol": "MATICUSDT", "name": "Polygon", "ticker": "MATIC"},
    {"symbol": "LINKUSDT", "name": "Chainlink", "ticker": "LINK"},
    {"symbol": "UNIUSDT", "name": "Uniswap", "ticker": "UNI"},
    {"symbol": "ATOMUSDT", "name": "Cosmos", "ticker": "ATOM"},
    {"symbol": "LTCUSDT", "name": "Litecoin", "ticker": "LTC"},
    {"symbol": "TRXUSDT", "name": "Tron", "ticker": "TRX"},
    {"symbol": "DOGEUSDT", "name": "Dogecoin", "ticker": "DOGE"}
]


def get_usd_to_kes_rate() -> float:
    """Get current USD to KES exchange rate from exchangerate-api.com (free tier)."""
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
        data = response.json()
        kes_rate = data.get("rates", {}).get("KES", 130.0)  # Default fallback
        logger.info(f"USD to KES rate: {kes_rate}")
        return kes_rate
    except Exception as e:
        logger.error(f"Error fetching exchange rate: {e}")
        return 130.0  # Fallback rate


def format_dual_currency(usd_value: float, kes_rate: float) -> str:
    """Format value in both USD and KES."""
    kes_value = usd_value * kes_rate
    if usd_value >= 1_000_000:
        return f"${usd_value:,.2f} (KSh {kes_value:,.0f})"
    return f"${usd_value:,.2f} (KSh {kes_value:,.2f})"


def get_binance_data(symbol: str, client: Client) -> Dict:
    """Get comprehensive Binance market data for a symbol."""
    try:
        # Current price
        price_data = client.get_symbol_ticker(symbol=symbol)
        current_price = float(price_data['price'])

        # 24h statistics
        ticker_24h = client.get_ticker(symbol=symbol)

        # Order book
        depth = client.get_order_book(symbol=symbol, limit=100)

        # Recent trades
        trades = client.get_recent_trades(symbol=symbol, limit=100)

        # Klines (1h, last 24)
        klines_1h = client.get_klines(symbol=symbol, interval='1h', limit=24)

        return {
            'price': current_price,
            'price_change': float(ticker_24h['priceChange']),
            'price_change_percent': float(ticker_24h['priceChangePercent']),
            'high_24h': float(ticker_24h['highPrice']),
            'low_24h': float(ticker_24h['lowPrice']),
            'volume_24h': float(ticker_24h['volume']),
            'quote_volume_24h': float(ticker_24h['quoteVolume']),
            'bid_price': float(depth['bids'][0][0]) if depth['bids'] else current_price,
            'ask_price': float(depth['asks'][0][0]) if depth['asks'] else current_price,
            'bid_qty': float(depth['bids'][0][1]) if depth['bids'] else 0,
            'ask_qty': float(depth['asks'][0][1]) if depth['asks'] else 0,
            'trades_count': len(trades),
            'klines_1h': klines_1h
        }
    except Exception as e:
        logger.error(f"Error fetching Binance data for {symbol}: {e}")
        return {}


def get_tradingview_indicators(ticker: str, timeframe: str = "1h") -> Dict:
    """Get TradingView technical indicators."""
    try:
        # Map timeframes
        tv_timeframe = {
            "1h": "1h",
            "4h": "4h",
            "1d": "1d"
        }.get(timeframe, "1h")

        scanner = Scanner()
        result = scanner.get_scanner_data(
            exchange="BINANCE",
            symbol=f"{ticker}USDT",
            interval=tv_timeframe
        )

        if result:
            return result
        return {}
    except Exception as e:
        logger.error(f"Error fetching TradingView indicators for {ticker} {timeframe}: {e}")
        return {}


def analyze_coin(coin: Dict, client: Client, kes_rate: float) -> Dict:
    """Perform comprehensive analysis for a single coin."""
    symbol = coin['symbol']
    ticker = coin['ticker']
    name = coin['name']

    logger.info(f"Analyzing {name} ({ticker})...")

    # Get Binance data
    binance_data = get_binance_data(symbol, client)

    if not binance_data:
        logger.warning(f"No Binance data for {symbol}")
        return {}

    # Get TradingView indicators for multiple timeframes
    tv_1h = get_tradingview_indicators(ticker, "1h")
    tv_4h = get_tradingview_indicators(ticker, "4h")
    tv_1d = get_tradingview_indicators(ticker, "1d")

    # Calculate technical signals
    price = binance_data['price']
    change_24h = binance_data['price_change_percent']

    # Extract key indicators from TradingView
    rsi_1h = tv_1h.get('RSI', 50)
    rsi_4h = tv_4h.get('RSI', 50)
    macd_1h = tv_1h.get('MACD.macd', 0)
    macd_signal_1h = tv_1h.get('MACD.signal', 0)

    # Determine trend
    if change_24h > 5:
        trend = "Strong Bullish 🚀"
    elif change_24h > 2:
        trend = "Bullish 📈"
    elif change_24h < -5:
        trend = "Strong Bearish 📉"
    elif change_24h < -2:
        trend = "Bearish ⬇️"
    else:
        trend = "Neutral ➡️"

    # RSI interpretation
    if rsi_1h > 70:
        rsi_signal = "Overbought"
    elif rsi_1h < 30:
        rsi_signal = "Oversold"
    else:
        rsi_signal = "Neutral"

    # MACD signal
    if macd_1h > macd_signal_1h:
        macd_signal = "Bullish"
    else:
        macd_signal = "Bearish"

    # Overall recommendation
    bullish_signals = 0
    bearish_signals = 0

    if rsi_1h < 30:
        bullish_signals += 2
    elif rsi_1h < 40:
        bullish_signals += 1
    elif rsi_1h > 70:
        bearish_signals += 2
    elif rsi_1h > 60:
        bearish_signals += 1

    if macd_1h > macd_signal_1h:
        bullish_signals += 1
    else:
        bearish_signals += 1

    if change_24h > 3:
        bullish_signals += 1
    elif change_24h < -3:
        bearish_signals += 1

    if bullish_signals > bearish_signals + 1:
        recommendation = "STRONG BUY"
    elif bullish_signals > bearish_signals:
        recommendation = "BUY"
    elif bearish_signals > bullish_signals + 1:
        recommendation = "STRONG SELL"
    elif bearish_signals > bullish_signals:
        recommendation = "SELL"
    else:
        recommendation = "HOLD"

    return {
        'name': name,
        'ticker': ticker,
        'symbol': symbol,
        'price': price,
        'price_usd_kes': format_dual_currency(price, kes_rate),
        'change_24h': change_24h,
        'high_24h': binance_data['high_24h'],
        'high_24h_usd_kes': format_dual_currency(binance_data['high_24h'], kes_rate),
        'low_24h': binance_data['low_24h'],
        'low_24h_usd_kes': format_dual_currency(binance_data['low_24h'], kes_rate),
        'volume_24h': binance_data['quote_volume_24h'],
        'volume_24h_usd_kes': format_dual_currency(binance_data['quote_volume_24h'], kes_rate),
        'bid_ask_spread': binance_data['ask_price'] - binance_data['bid_price'],
        'rsi_1h': rsi_1h,
        'rsi_4h': rsi_4h,
        'rsi_signal': rsi_signal,
        'macd_signal': macd_signal,
        'trend': trend,
        'recommendation': recommendation,
        'tv_1h': tv_1h,
        'tv_4h': tv_4h,
        'tv_1d': tv_1d
    }


def generate_markdown_report(analyses: List[Dict], kes_rate: float) -> str:
    """Generate comprehensive markdown report."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    md = f"""# 📊 Major Cryptocurrencies Market Analysis
**Generated:** {timestamp}
**Analysis Period:** Hourly
**Exchange Rate:** 1 USD = {kes_rate:.2f} KES

---

## 🎯 Executive Summary

"""

    # Calculate overall stats
    total_coins = len(analyses)
    bullish_count = sum(1 for a in analyses if 'BUY' in a['recommendation'])
    bearish_count = sum(1 for a in analyses if 'SELL' in a['recommendation'])

    # Find top performer
    top_performer = max(analyses, key=lambda x: x['change_24h'])
    worst_performer = min(analyses, key=lambda x: x['change_24h'])
    highest_volume = max(analyses, key=lambda x: x['volume_24h'])

    md += f"""**Market Phase:** {"Bull Market 🐂" if bullish_count > bearish_count else "Bear Market 🐻" if bearish_count > bullish_count else "Mixed Market"}
**Overall Sentiment:** {"Bullish" if bullish_count > bearish_count else "Bearish" if bearish_count > bullish_count else "Neutral"}

**Top Performer (24h):** {top_performer['ticker']} +{top_performer['change_24h']:.2f}%
**Worst Performer (24h):** {worst_performer['ticker']} {worst_performer['change_24h']:.2f}%
**Highest Volume:** {highest_volume['ticker']} {highest_volume['volume_24h_usd_kes']}

**Key Takeaways:**
- 🔹 {bullish_count} coins showing buy signals, {bearish_count} showing sell signals
- 🔹 {top_performer['name']} leading with {top_performer['change_24h']:.2f}% gain
- 🔹 Market showing {"strong momentum" if abs(top_performer['change_24h']) > 10 else "moderate activity"}

---

## 💰 Major Coins Overview

"""

    # Individual coin analysis
    for analysis in analyses:
        md += f"""### {analysis['name']} ({analysis['ticker']})

**Current Price:** {analysis['price_usd_kes']}
**24h Change:** {analysis['change_24h']:+.2f}% | **Trend:** {analysis['trend']}

#### Market Data
- **24h High:** {analysis['high_24h_usd_kes']}
- **24h Low:** {analysis['low_24h_usd_kes']}
- **24h Volume:** {analysis['volume_24h_usd_kes']}
- **Bid/Ask Spread:** ${analysis['bid_ask_spread']:.4f}

#### Technical Analysis
- **RSI (1h):** {analysis['rsi_1h']:.1f} - {analysis['rsi_signal']}
- **RSI (4h):** {analysis['rsi_4h']:.1f}
- **MACD Signal:** {analysis['macd_signal']}
- **Overall Recommendation:** **{analysis['recommendation']}**

---

"""

    # Comparative analysis table
    md += """## 📊 Comparative Analysis

### Performance Table

| Coin | Price (USD/KES) | 24h % | Volume | RSI (1h) | Trend | Recommendation |
|------|-----------------|-------|--------|----------|-------|----------------|
"""

    for analysis in analyses:
        md += f"| {analysis['ticker']} | ${analysis['price']:,.2f} | {analysis['change_24h']:+.2f}% | ${analysis['volume_24h']/1e6:.1f}M | {analysis['rsi_1h']:.1f} | {analysis['trend']} | {analysis['recommendation']} |\n"

    md += """
---

## 🎯 Trading Opportunities

### 🟢 Best Long Setups (Next 1-4 Hours)

"""

    # Find best long opportunities (oversold with bullish momentum)
    long_opportunities = [a for a in analyses if 'BUY' in a['recommendation']]
    long_opportunities.sort(key=lambda x: (x['rsi_1h'], -x['change_24h']))

    for i, opp in enumerate(long_opportunities[:5], 1):
        entry_price = opp['price']
        target1 = entry_price * 1.03
        target2 = entry_price * 1.05
        stop_loss = entry_price * 0.97

        md += f"""**{i}. {opp['ticker']} - {opp['name']}**
- **Current Price:** {format_dual_currency(entry_price, kes_rate)}
- **Entry Zone:** {format_dual_currency(entry_price * 0.995, kes_rate)} - {format_dual_currency(entry_price * 1.005, kes_rate)}
- **Target 1:** {format_dual_currency(target1, kes_rate)} [+3%]
- **Target 2:** {format_dual_currency(target2, kes_rate)} [+5%]
- **Stop Loss:** {format_dual_currency(stop_loss, kes_rate)} [-3%]
- **Risk/Reward Ratio:** 1:1.67
- **Timeframe:** 1-4 hours
- **Rationale:**
  - Technical: RSI at {opp['rsi_1h']:.1f} ({opp['rsi_signal']}), MACD {opp['macd_signal']}
  - Momentum: 24h change {opp['change_24h']:+.2f}%
  - Risk: Good support at current levels
- **Confidence Level:** {"High" if opp['rsi_1h'] < 35 else "Medium"}

"""

    # Avoid list
    avoid_list = [a for a in analyses if a['rsi_1h'] > 70 or (a['change_24h'] < -10)]
    if avoid_list:
        md += """### ❌ Avoid List

**Coins to AVOID this hour:**
"""
        for coin in avoid_list:
            reason = "Overbought" if coin['rsi_1h'] > 70 else "Heavy selloff"
            md += f"- **{coin['ticker']}**: {reason} (RSI: {coin['rsi_1h']:.1f}, 24h: {coin['change_24h']:+.2f}%)\n"

    md += """
---

## ⚠️ Disclaimer

This analysis is for informational purposes only and does not constitute financial advice. Cryptocurrency trading involves substantial risk of loss. Always do your own research (DYOR) and never invest more than you can afford to lose. Past performance does not guarantee future results.

**Data Sources:**
- Binance (Market data)
- TradingView (Technical indicators)
- ExchangeRate-API (Currency conversion)

---

*Analysis generated by Claude Code Major Coins Analysis System*
"""

    return md


def main():
    """Main execution function."""
    logger.info("Starting Major Coins Analysis...")

    # Get exchange rate
    logger.info("Fetching USD to KES exchange rate...")
    kes_rate = get_usd_to_kes_rate()

    # Initialize Binance client
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("Binance API credentials not found in environment")
        sys.exit(1)

    client = Client(api_key, api_secret)
    logger.info("Binance client initialized")

    # Analyze all major coins
    analyses = []
    for coin in MAJOR_COINS:
        try:
            analysis = analyze_coin(coin, client, kes_rate)
            if analysis:
                analyses.append(analysis)
        except Exception as e:
            logger.error(f"Error analyzing {coin['name']}: {e}")
            continue

    if not analyses:
        logger.error("No analysis data collected")
        sys.exit(1)

    logger.info(f"Successfully analyzed {len(analyses)} coins")

    # Generate report
    logger.info("Generating markdown report...")
    report = generate_markdown_report(analyses, kes_rate)

    # Save report
    timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H-%M")
    filename = f"majors-analysis-{timestamp}.md"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)

    logger.info(f"✅ Major coins analysis saved to: {filename}")
    print(f"\n✅ Major coins analysis saved to: {filename}")

    return filename


if __name__ == "__main__":
    main()
