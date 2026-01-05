"""
Coinlist Integration Example
---------------------------
Demonstrates how to use the coinlist module to load symbols from files
and fetch trading signals.
"""

import logging
from coinlist import load_symbols, list_available_exchanges, save_symbols
from trading_screener import get_trading_signals
from trading_utils import setup_logging

# Setup logging
logger = setup_logging()

def example_load_from_file():
    """Example: Load symbols from file and analyze them."""
    print("🚀 Coinlist Integration Example\n")
    
    # List available exchanges
    exchanges = list_available_exchanges()
    print(f"📁 Available exchange symbol lists: {exchanges}\n")
    
    if not exchanges:
        print("❌ No symbol lists found in coinlist directory.")
        print("💡 Create a file like 'coinlist/BINANCE.txt' with symbols (one per line)")
        return
    
    # Load symbols for first available exchange
    exchange = exchanges[0]
    symbols = load_symbols(exchange)
    
    print(f"📊 Loaded {len(symbols)} symbols from {exchange}")
    print(f"   First 5: {symbols[:5]}\n")
    
    # Analyze first 3 symbols
    print(f"🔍 Analyzing first 3 symbols from {exchange}...\n")
    
    results = get_trading_signals(
        exchange=exchange,
        symbols=symbols[:3],
        timeframe="4h"
    )
    
    if results:
        print(f"{'SYMBOL':<20} {'PRICE':<12} {'RATING':<10} {'SIGNAL':<15}")
        print("-" * 80)
        
        for res in results:
            symbol = res['symbol']
            price = res['metrics']['price']
            rating = res['rating']
            signal = res['signal']
            
            print(f"{symbol:<20} ${price:<11.4f} {rating:<10} {signal:<15}")
    else:
        print("❌ No results returned")

def example_save_custom_list():
    """Example: Create and save a custom symbol list."""
    print("\n" + "="*80)
    print("💾 Creating custom symbol list...\n")
    
    custom_symbols = [
        "BINANCE:BTCUSDT",
        "BINANCE:ETHUSDT",
        "BINANCE:SOLUSDT",
    ]
    
    success = save_symbols("CUSTOM", custom_symbols)
    
    if success:
        print(f"✅ Saved {len(custom_symbols)} symbols to coinlist/CUSTOM.txt")
        
        # Load it back
        loaded = load_symbols("CUSTOM")
        print(f"✅ Verified: Loaded {len(loaded)} symbols back")
    else:
        print("❌ Failed to save symbols")

if __name__ == "__main__":
    example_load_from_file()
    example_save_custom_list()
