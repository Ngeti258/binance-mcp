"""
Complete Indicators Demo
-----------------------
Demonstrates ALL indicators including CCI that are fetched and analyzed.
"""

import logging
from trading_screener import get_trading_signals
from trading_utils import setup_logging, get_full_analysis

# Setup logging
logger = setup_logging()

def main():
    print("🚀 Complete Indicators Demonstration\n")
    print("This demo shows ALL indicators: BB, StochRSI, MACD, ADX, and CCI\n")
    
    # Configuration
    exchange = "BINANCE"
    symbols = ["BINANCE:BTCUSDT"]
    timeframe = "4h"
    
    print(f"📊 Analyzing {symbols[0]} on {timeframe} timeframe...\n")
    
    try:
        results = get_trading_signals(exchange, symbols, timeframe)
        
        if not results:
            print("❌ No results found.")
            return
        
        # Get the first result
        result = results[0]
        metrics = result['metrics']
        
        # Display comprehensive analysis
        print("="*80)
        print(f"📈 SYMBOL: {result['symbol']}")
        print(f"💰 PRICE: ${metrics['price']:.4f}")
        print(f"📊 OVERALL SIGNAL: {result['signal']} (Rating: {result['rating']})")
        print("="*80)
        
        # Show ALL individual indicators
        indicators = metrics['indicators']
        
        print("\n🎯 BOLLINGER BANDS")
        bb = indicators['bollinger_bands']
        print(f"   Signal: {bb['signal']} (Rating: {bb['rating']})")
        print(f"   Width: {bb['width']:.4f}")
        print(f"   Position: {bb['position']}")
        print(f"   Bands: Lower={bb['lower']:.4f} | Middle={bb['middle']:.4f} | Upper={bb['upper']:.4f}")
        
        print("\n📈 STOCHASTIC RSI")
        stoch = indicators['stochastic_rsi']
        print(f"   Signal: {stoch['signal']} (Rating: {stoch['rating']})")
        print(f"   K: {stoch['k']:.2f}")
        print(f"   D: {stoch['d']:.2f}")
        print(f"   Position: {stoch['position']}")
        
        print("\n📉 MACD")
        macd = indicators['macd']
        print(f"   Signal: {macd['signal']} (Rating: {macd['rating']})")
        print(f"   MACD: {macd['value']:.4f}")
        print(f"   Signal Line: {macd['signal_line']:.4f}")
        print(f"   Histogram: {macd['histogram']:.4f}")
        print(f"   Position: {macd['position']}")
        
        print("\n💪 ADX (Trend Strength)")
        adx = indicators['adx']
        print(f"   Signal: {adx['signal']} (Rating: {adx['rating']})")
        print(f"   ADX: {adx['value']:.2f}")
        print(f"   +DI: {adx['plus_di']:.2f}")
        print(f"   -DI: {adx['minus_di']:.2f}")
        print(f"   Trend Strength: {adx['trend_strength']:.2f}")
        print(f"   Trend Quality: {adx['trend_quality']}")
        
        print("\n🔄 CCI (Commodity Channel Index)")
        cci = indicators['cci']
        print(f"   Signal: {cci['signal']} (Rating: {cci['rating']})")
        print(f"   Value: {cci['value']:.2f}")
        print(f"   Position: {cci['position']}")
        
        print("\n" + "="*80)
        print("📊 COMPOSITE ANALYSIS")
        print("="*80)
        composite = metrics['composite']
        breakdown = composite['breakdown']
        print(f"   Raw Score: {breakdown['raw_score']:.2f}")
        print(f"   Bullish Indicators: {breakdown['bullish_indicators']}")
        print(f"   Bearish Indicators: {breakdown['bearish_indicators']}")
        print(f"   Neutral Indicators: {breakdown['neutral_indicators']}")
        print(f"   Total Indicators: {breakdown['total_indicators']}")
        
        print("\n✅ All 5 indicators successfully fetched and displayed!")
        print("   ✓ Bollinger Bands")
        print("   ✓ Stochastic RSI")
        print("   ✓ MACD")
        print("   ✓ ADX")
        print("   ✓ CCI")
        
    except ImportError:
        print("\n❌ Error: 'tradingview-screener' package is missing.")
        print("Please install it using: pip install tradingview-screener")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logging.exception("Detailed error:")

if __name__ == "__main__":
    main()
