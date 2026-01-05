"""
Screener Integration Example
--------------------------
Demonstrates how to use the improved trading_screener module to fetch data
and generate trading signals.
"""

import logging
import sys
from trading_screener import get_trading_signals, fetch_screener_indicators
from trading_utils import setup_logging

# Setup logging
logger = setup_logging()

def main():
    print("🚀 Starting Screener Integration Test...")
    
    # Configuration
    exchange = "BINANCE"
    # Test with some major pairs
    symbols = [
        "BINANCE:BTCUSDT", 
        "BINANCE:ETHUSDT", 
        "BINANCE:SOLUSDT",
        "BINANCE:BNBUSDT",
        "BINANCE:XRPUSDT"
    ]
    timeframe = "4h"
    
    print(f"\n📊 Fetching data for {len(symbols)} symbols on {timeframe} timeframe...")
    
    try:
        # Use the high-level function that integrates everything
        results = get_trading_signals(exchange, symbols, timeframe)
        
        if not results:
            print("❌ No results found. Check your internet connection or symbol names.")
            return
            
        print(f"\n✅ Successfully analyzed {len(results)} symbols:\n")
        
        # Print results in a nice table
        print(f"{'SYMBOL':<20} {'PRICE':<12} {'RATING':<10} {'SIGNAL':<15}")
        print("-" * 80)
        
        for res in results:
            symbol = res['symbol']
            metrics = res['metrics']
            price = metrics['price']  # This is a float, not a dict
            rating = res['rating']
            signal = res['signal']
            
            # Color code based on signal (if terminal supports it, otherwise plain text)
            print(f"{symbol:<20} ${price:<11.4f} {rating:<10} {signal:<15}")
            
            # Print detailed breakdown for the first symbol as example
            if symbol == symbols[0]:
                print("\n🔍 Detailed Breakdown for first symbol:")
                bb = metrics['indicators']['bollinger_bands']
                stoch = metrics['indicators']['stochastic_rsi']
                macd = metrics['indicators']['macd']
                adx = metrics['indicators']['adx']
                
                print(f"   BB Width: {bb['width']:.4f}")
                print(f"   StochRSI: K={stoch['k']:.2f}, D={stoch['d']:.2f}")
                print(f"   MACD Histogram: {macd['histogram']:.4f}")
                print(f"   ADX: {adx['value']:.2f}")
                print("-" * 80)
                
    except ImportError:
        print("\n❌ Error: 'tradingview-screener' package is missing.")
        print("Please install it using: pip install tradingview-screener")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logging.exception("Detailed error:")

if __name__ == "__main__":
    main()
