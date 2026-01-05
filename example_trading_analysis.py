"""
Example Usage of Trading Metrics System
Demonstrates how to use the trading analysis modules.
"""

from trading_metrics import compute_metrics
from trading_utils import get_full_analysis, setup_logging
from trading_constants import DEFAULT_WEIGHTS
import logging


def example_bullish_scenario():
    """Example with bullish indicators"""
    print("\n" + "=" * 60)
    print("EXAMPLE 1: BULLISH SCENARIO")
    print("=" * 60)
    
    indicators = {
        # Price data
        "open": 100.0,
        "close": 102.5,  # Price up 2.5%
        
        # Bollinger Bands - price in lower band (oversold)
        "SMA20": 101.0,
        "BB.upper": 105.0,
        "BB.lower": 97.0,
        
        # Stochastic RSI - oversold
        "StochRSI.K": 15.0,  # Oversold
        "StochRSI.D": 18.0,
        
        # MACD - bullish crossover
        "MACD": 0.5,
        "MACD.signal": 0.3,
        "MACD.histogram": 0.2,
        
        # ADX - strong uptrend
        "ADX": 35.0,
        "ADX.plus_di": 30.0,
        "ADX.minus_di": 15.0,
        
        # CCI - oversold
        "CCI": -150.0,
    }
    
    result = compute_metrics(indicators)
    if result:
        print(get_full_analysis(result))
    else:
        print("❌ Failed to compute metrics")


def example_bearish_scenario():
    """Example with bearish indicators"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: BEARISH SCENARIO")
    print("=" * 60)
    
    indicators = {
        # Price data
        "open": 100.0,
        "close": 97.5,  # Price down 2.5%
        
        # Bollinger Bands - price above upper band (overbought)
        "SMA20": 99.0,
        "BB.upper": 103.0,
        "BB.lower": 95.0,
        
        # Stochastic RSI - overbought
        "StochRSI.K": 85.0,  # Overbought
        "StochRSI.D": 82.0,
        
        # MACD - bearish crossover
        "MACD": -0.4,
        "MACD.signal": -0.2,
        "MACD.histogram": -0.2,
        
        # ADX - strong downtrend
        "ADX": 32.0,
        "ADX.plus_di": 12.0,
        "ADX.minus_di": 28.0,
        
        # CCI - overbought
        "CCI": 180.0,
    }
    
    result = compute_metrics(indicators)
    if result:
        print(get_full_analysis(result))
    else:
        print("❌ Failed to compute metrics")


def example_neutral_scenario():
    """Example with mixed/neutral indicators"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: NEUTRAL/MIXED SCENARIO")
    print("=" * 60)
    
    indicators = {
        # Price data
        "open": 100.0,
        "close": 100.2,  # Price flat
        
        # Bollinger Bands - price at middle
        "SMA20": 100.0,
        "BB.upper": 104.0,
        "BB.lower": 96.0,
        
        # Stochastic RSI - neutral
        "StochRSI.K": 50.0,
        "StochRSI.D": 48.0,
        
        # MACD - weak signal
        "MACD": 0.1,
        "MACD.signal": 0.05,
        "MACD.histogram": 0.05,
        
        # ADX - weak trend
        "ADX": 18.0,
        "ADX.plus_di": 20.0,
        "ADX.minus_di": 19.0,
        
        # CCI - neutral
        "CCI": 10.0,
    }
    
    result = compute_metrics(indicators)
    if result:
        print(get_full_analysis(result))
    else:
        print("❌ Failed to compute metrics")


def example_custom_weights():
    """Example with custom indicator weights"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: CUSTOM WEIGHTS (Emphasize MACD & StochRSI)")
    print("=" * 60)
    
    indicators = {
        "open": 100.0,
        "close": 102.0,
        "SMA20": 101.0,
        "BB.upper": 105.0,
        "BB.lower": 97.0,
        "StochRSI.K": 25.0,
        "StochRSI.D": 30.0,
        "MACD": 0.6,
        "MACD.signal": 0.3,
        "MACD.histogram": 0.3,
        "ADX": 28.0,
        "ADX.plus_di": 25.0,
        "ADX.minus_di": 15.0,
        "CCI": -80.0,
    }
    
    # Custom weights - emphasize momentum indicators
    custom_weights = {
        "bb": 0.8,
        "stoch_rsi": 1.5,  # Higher weight
        "macd": 1.5,       # Higher weight
        "adx": 0.7,
        "cci": 0.9,
    }
    
    print("\nUsing custom weights:")
    for indicator, weight in custom_weights.items():
        print(f"  {indicator}: {weight}")
    
    result = compute_metrics(indicators, weights=custom_weights)
    if result:
        print(get_full_analysis(result))
    else:
        print("❌ Failed to compute metrics")


def example_validation_error():
    """Example showing validation catching invalid data"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: VALIDATION ERROR HANDLING")
    print("=" * 60)
    
    # Invalid data - StochRSI out of range
    invalid_indicators = {
        "open": 100.0,
        "close": 102.0,
        "SMA20": 101.0,
        "BB.upper": 105.0,
        "BB.lower": 97.0,
        "StochRSI.K": 150.0,  # ❌ INVALID - must be 0-100
        "StochRSI.D": 30.0,
        "MACD": 0.5,
        "MACD.signal": 0.3,
        "MACD.histogram": 0.2,
        "ADX": 28.0,
        "ADX.plus_di": 25.0,
        "ADX.minus_di": 15.0,
        "CCI": -50.0,
    }
    
    print("\nAttempting to compute metrics with invalid StochRSI.K = 150.0...")
    result = compute_metrics(invalid_indicators)
    if result:
        print("✅ Metrics computed (unexpected)")
    else:
        print("❌ Validation correctly rejected invalid data")
        print("Check logs for error details")


def main():
    """Run all examples"""
    # Setup logging
    setup_logging(level=logging.INFO)
    
    print("\n" + "=" * 60)
    print("TRADING METRICS SYSTEM - EXAMPLES")
    print("=" * 60)
    print("\nThis script demonstrates the trading analysis system")
    print("with various market scenarios.\n")
    
    # Run examples
    example_bullish_scenario()
    example_bearish_scenario()
    example_neutral_scenario()
    example_custom_weights()
    example_validation_error()
    
    print("\n" + "=" * 60)
    print("EXAMPLES COMPLETE")
    print("=" * 60)
    print("\n💡 Tips:")
    print("  • Adjust weights in trading_constants.py to tune the system")
    print("  • All thresholds are configurable in trading_constants.py")
    print("  • Enable DEBUG logging to see detailed calculations")
    print("  • Always validate your indicator data before trading")
    print("  • Paper trade before using with real money!")
    print("\n")


if __name__ == "__main__":
    main()
