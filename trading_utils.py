"""
Trading Utility Functions
Helper functions for formatting, recommendations, and analysis.
"""

from __future__ import annotations
from typing import Dict, Optional
import logging
from datetime import datetime, timezone

from trading_constants import Signal, TREND_STRENGTH_MODERATE, TREND_STRENGTH_WEAK

logger = logging.getLogger(__name__)


def get_trading_recommendation(metrics: Dict) -> str:
    """
    Generate a human-readable trading recommendation from metrics.
    
    Args:
        metrics: Dictionary returned from compute_metrics()
    
    Returns:
        Formatted recommendation string
    """
    if not metrics:
        return "❌ Unable to generate recommendation - insufficient data"
    
    composite = metrics["composite"]
    signal = composite["signal"]
    rating = composite["rating"]
    trend_strength = composite["trend_strength"]
    breakdown = composite["breakdown"]
    
    bullish = breakdown["bullish_indicators"]
    bearish = breakdown["bearish_indicators"]
    neutral = breakdown["neutral_indicators"]
    raw_score = breakdown["raw_score"]
    
    # Build recommendation
    lines = []
    lines.append("=" * 50)
    lines.append("📊 TRADING RECOMMENDATION")
    lines.append("=" * 50)
    
    # Signal and rating
    signal_emoji = {
        Signal.STRONG_BUY.value: "🟢🟢",
        Signal.BUY.value: "🟢",
        Signal.NEUTRAL.value: "⚪",
        Signal.SELL.value: "🔴",
        Signal.STRONG_SELL.value: "🔴🔴",
    }
    
    lines.append(f"\n{signal_emoji.get(signal, '⚪')} Signal: {signal}")
    lines.append(f"📈 Rating: {rating}/3 (Raw Score: {raw_score})")
    
    # Trend strength
    if trend_strength > TREND_STRENGTH_MODERATE:
        trend_desc = "Strong 💪"
    elif trend_strength > TREND_STRENGTH_WEAK:
        trend_desc = "Moderate 👍"
    else:
        trend_desc = "Weak 🤏"
    lines.append(f"📉 Trend Strength: {trend_desc} ({trend_strength:.2f})")
    
    # Consensus
    lines.append(f"\n🔍 Indicator Consensus:")
    lines.append(f"   • {bullish} Bullish")
    lines.append(f"   • {bearish} Bearish")
    lines.append(f"   • {neutral} Neutral")
    
    # Action recommendation
    lines.append(f"\n💡 Recommended Action:")
    if signal == Signal.STRONG_BUY.value:
        lines.append("   ✅ STRONG BUY - Consider entering long positions")
        lines.append("   ✅ High conviction bullish signal")
    elif signal == Signal.BUY.value:
        lines.append("   ✅ BUY - Consider long positions or hold existing longs")
        lines.append("   ✅ Moderate bullish signal")
    elif signal == Signal.SELL.value:
        lines.append("   ⚠️ SELL - Consider closing longs or entering shorts")
        lines.append("   ⚠️ Moderate bearish signal")
    elif signal == Signal.STRONG_SELL.value:
        lines.append("   🛑 STRONG SELL - Consider closing longs or shorting")
        lines.append("   🛑 High conviction bearish signal")
    else:
        lines.append("   ➡️ NEUTRAL - Hold current positions")
        lines.append("   ➡️ Wait for clearer signals before acting")
    
    # Risk warning
    lines.append(f"\n⚠️ Risk Assessment:")
    if trend_strength < TREND_STRENGTH_WEAK:
        lines.append("   • Low trend strength - choppy market conditions")
        lines.append("   • Consider reducing position sizes")
    
    if abs(rating) <= 1:
        lines.append("   • Weak signal - low conviction")
        lines.append("   • Wait for confirmation before acting")
    
    if bullish > 0 and bearish > 0:
        lines.append("   • Mixed signals - indicators disagree")
        lines.append("   • Exercise caution")
    
    lines.append("=" * 50)
    
    return "\n".join(lines)


def format_indicator_details(metrics: Dict) -> str:
    """
    Format detailed breakdown of individual indicators.
    
    Args:
        metrics: Dictionary returned from compute_metrics()
    
    Returns:
        Formatted indicator details string
    """
    if not metrics or "indicators" not in metrics:
        return "No indicator data available"
    
    indicators = metrics["indicators"]
    lines = []
    
    lines.append("\n" + "=" * 50)
    lines.append("📊 INDIVIDUAL INDICATOR DETAILS")
    lines.append("=" * 50)
    
    # Bollinger Bands
    bb = indicators.get("bollinger_bands", {})
    lines.append(f"\n🎯 Bollinger Bands:")
    lines.append(f"   Signal: {bb.get('signal', 'N/A')} (Rating: {bb.get('rating', 0)})")
    lines.append(f"   Position: {bb.get('position', 'N/A')}")
    lines.append(f"   Width: {bb.get('width', 'N/A')}")
    lines.append(f"   Bands: {bb.get('lower', 'N/A')} | {bb.get('middle', 'N/A')} | {bb.get('upper', 'N/A')}")
    
    # Stochastic RSI
    stoch = indicators.get("stochastic_rsi", {})
    lines.append(f"\n📈 Stochastic RSI:")
    lines.append(f"   Signal: {stoch.get('signal', 'N/A')} (Rating: {stoch.get('rating', 0)})")
    lines.append(f"   Position: {stoch.get('position', 'N/A')}")
    lines.append(f"   K: {stoch.get('k', 'N/A')}, D: {stoch.get('d', 'N/A')}")
    
    # MACD
    macd = indicators.get("macd", {})
    lines.append(f"\n📉 MACD:")
    lines.append(f"   Signal: {macd.get('signal', 'N/A')} (Rating: {macd.get('rating', 0)})")
    lines.append(f"   Position: {macd.get('position', 'N/A')}")
    lines.append(f"   MACD: {macd.get('value', 'N/A')}")
    lines.append(f"   Signal Line: {macd.get('signal_line', 'N/A')}")
    lines.append(f"   Histogram: {macd.get('histogram', 'N/A')}")
    
    # ADX
    adx = indicators.get("adx", {})
    lines.append(f"\n💪 ADX (Trend Strength):")
    lines.append(f"   Signal: {adx.get('signal', 'N/A')} (Rating: {adx.get('rating', 0)})")
    lines.append(f"   Trend Quality: {adx.get('trend_quality', 'N/A')}")
    lines.append(f"   ADX: {adx.get('value', 'N/A')}")
    lines.append(f"   +DI: {adx.get('plus_di', 'N/A')}, -DI: {adx.get('minus_di', 'N/A')}")
    lines.append(f"   Trend Strength: {adx.get('trend_strength', 'N/A')}")
    
    # CCI
    cci = indicators.get("cci", {})
    lines.append(f"\n🔄 CCI (Commodity Channel Index):")
    lines.append(f"   Signal: {cci.get('signal', 'N/A')} (Rating: {cci.get('rating', 0)})")
    lines.append(f"   Position: {cci.get('position', 'N/A')}")
    lines.append(f"   Value: {cci.get('value', 'N/A')}")
    
    lines.append("=" * 50)
    
    return "\n".join(lines)


def format_price_info(metrics: Dict) -> str:
    """
    Format basic price information.
    
    Args:
        metrics: Dictionary returned from compute_metrics()
    
    Returns:
        Formatted price info string
    """
    if not metrics:
        return "No price data available"
    
    price = metrics.get("price", "N/A")
    change = metrics.get("change", 0)
    
    change_emoji = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
    change_sign = "+" if change > 0 else ""
    
    lines = []
    lines.append("=" * 50)
    lines.append("💰 PRICE INFORMATION")
    lines.append("=" * 50)
    lines.append(f"Current Price: ${price}")
    lines.append(f"Change: {change_emoji} {change_sign}{change}%")
    lines.append("=" * 50)
    
    return "\n".join(lines)


def get_full_analysis(metrics: Dict) -> str:
    """
    Generate a complete analysis report combining all information.
    
    Args:
        metrics: Dictionary returned from compute_metrics()
    
    Returns:
        Complete formatted analysis
    """
    if not metrics:
        return "❌ Unable to generate analysis - no metrics available"
    
    sections = [
        format_price_info(metrics),
        get_trading_recommendation(metrics),
        format_indicator_details(metrics),
    ]
    
    return "\n\n".join(sections)



def generate_majors_report(results: list, prices: Dict[str, float]) -> str:
    """
    Generate a comprehensive Markdown report for major cryptocurrencies.
    
    Args:
        results: List of analysis results from trading_screener
        prices: Dictionary of current prices from Binance
        
    Returns:
        Formatted Markdown report string
    """
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%d %H:%M UTC")
    
    # Calculate market stats
    total_coins = len(results)
    bullish_count = sum(1 for r in results if "BUY" in r['signal'])
    bearish_count = sum(1 for r in results if "SELL" in r['signal'])
    neutral_count = total_coins - bullish_count - bearish_count
    
    # Sort by performance (change)
    sorted_results = sorted(results, key=lambda x: x['metrics'].get('change', 0), reverse=True)
    top_performer = sorted_results[0] if sorted_results else None
    worst_performer = sorted_results[-1] if sorted_results else None
    
    # Determine overall sentiment
    if bullish_count > bearish_count + neutral_count:
        sentiment = "Bullish"
        phase = "Market Expansion"
    elif bearish_count > bullish_count + neutral_count:
        sentiment = "Bearish"
        phase = "Market Correction"
    else:
        sentiment = "Neutral/Mixed"
        phase = "Consolidation"

    lines = []
    
    # Header
    lines.append(f"# 📊 Major Cryptocurrencies Market Analysis")
    lines.append(f"**Generated:** {timestamp}")
    lines.append(f"**Analysis Period:** 4h")
    lines.append(f"**Coins Analyzed:** {total_coins}")
    lines.append("\n---\n")
    
    # Executive Summary
    lines.append("## 🎯 Executive Summary\n")
    lines.append(f"**Market Phase:** {phase}")
    lines.append(f"**Overall Sentiment:** {sentiment}")
    if top_performer:
        top_change = top_performer['metrics'].get('change', 0)
        lines.append(f"**Top Performer:** {top_performer['symbol']} ({top_change:+.2f}%)")
    if worst_performer:
        worst_change = worst_performer['metrics'].get('change', 0)
        lines.append(f"**Worst Performer:** {worst_performer['symbol']} ({worst_change:+.2f}%)")
    
    lines.append("\n**Key Takeaways:**")
    lines.append(f"- {bullish_count} coins showing Bullish signals")
    lines.append(f"- {bearish_count} coins showing Bearish signals")
    lines.append(f"- {neutral_count} coins are Neutral")
    lines.append("\n---\n")
    
    # Detailed Coin Analysis
    lines.append("## 💰 Major Coins Overview\n")
    
    for result in results:
        symbol = result['symbol']
        metrics = result['metrics']
        signal = result['signal']
        rating = result['rating']
        price = prices.get(symbol, metrics.get('price', 0))
        change = metrics.get('change', 0)
        
        # Determine emoji
        if "STRONG_BUY" in signal: emoji = "🟢🟢"
        elif "BUY" in signal: emoji = "🟢"
        elif "STRONG_SELL" in signal: emoji = "🔴🔴"
        elif "SELL" in signal: emoji = "🔴"
        else: emoji = "⚪"
        
        lines.append(f"### {symbol} {emoji}")
        lines.append(f"- **Price:** ${price:,.4f}")
        lines.append(f"- **24h Change:** {change:+.2f}%")
        lines.append(f"- **Signal:** {signal} (Rating: {rating}/3)")
        
        # Technicals
        indicators = metrics.get('indicators', {})
        rsi = indicators.get('stochastic_rsi', {}).get('k', 'N/A')
        macd = indicators.get('macd', {}).get('value', 'N/A')
        
        lines.append(f"- **Technicals:** RSI(k)={rsi}, MACD={macd}")
        lines.append(f"- **Recommendation:** {get_trading_recommendation(metrics).splitlines()[-1].strip()}") # Extract just the action
        lines.append("\n")

    lines.append("---\n")
    
    # Comparative Table
    lines.append("## 📊 Comparative Analysis\n")
    lines.append("| Coin | Price | Change | Signal | Rating |")
    lines.append("|------|-------|--------|--------|--------|")
    
    for r in sorted_results:
        s = r['symbol'].replace("BINANCE:", "")
        p = prices.get(r['symbol'], r['metrics'].get('price', 0))
        c = r['metrics'].get('change', 0)
        sig = r['signal']
        rat = r['rating']
        lines.append(f"| **{s}** | ${p:,.4f} | {c:+.2f}% | {sig} | {rat} |")
        
    return "\n".join(lines)


def setup_logging(level: int = logging.INFO, log_file: Optional[str] = None) -> None:
    """
    Configure logging for the trading system.
    
    Args:
        level: Logging level (default: INFO)
        log_file: Optional file path to write logs to
    """
    handlers = [logging.StreamHandler()]
    
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
    
    logger.info("Trading system logging configured")
