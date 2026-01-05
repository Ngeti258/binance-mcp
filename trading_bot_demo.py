"""
Trading Bot Example
-----------------
Combines TradingView screener analysis with Binance API integration.
Demonstrates a complete trading workflow.
"""

import logging
from coinlist import load_symbols
from trading_screener import get_trading_signals
from binance_integration import BinanceIntegration, normalize_symbol, get_binance_prices
from trading_utils import setup_logging

# Setup logging
logger = setup_logging()

def analyze_and_trade_demo():
    """
    Demo: Analyze symbols using screener and check prices on Binance.
    """
    print("🤖 Trading Bot Demo - Screener + Binance Integration\n")
    print("="*80)
    
    # Step 1: Load symbols from file
    print("\n📁 Step 1: Loading symbols from coinlist...")
    symbols = load_symbols("BINANCE")
    
    if not symbols:
        print("❌ No symbols found. Using default list.")
        symbols = ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:SOLUSDT"]
    
    print(f"✅ Loaded {len(symbols)} symbols")
    print(f"   Analyzing first 5: {symbols[:5]}\n")
    
    # Step 2: Get trading signals from screener
    print("📊 Step 2: Fetching indicators and generating signals...")
    results = get_trading_signals(
        exchange="BINANCE",
        symbols=symbols[:5],
        timeframe="4h"
    )
    
    if not results:
        print("❌ No analysis results. Exiting.")
        return
    
    print(f"✅ Analyzed {len(results)} symbols\n")
    
    # Step 3: Get live prices from Binance
    print("💰 Step 3: Fetching live prices from Binance...")
    try:
        prices = get_binance_prices(symbols[:5])
        print(f"✅ Fetched {len(prices)} prices\n")
    except Exception as e:
        print(f"⚠️ Could not fetch Binance prices: {e}")
        print("   Continuing with screener prices...\n")
        prices = {}
    
    # Step 4: Display combined analysis
    print("="*80)
    print("📈 COMBINED ANALYSIS - Screener Signals + Binance Prices")
    print("="*80)
    print(f"{'SYMBOL':<20} {'SCREENER $':<15} {'BINANCE $':<15} {'SIGNAL':<15} {'RATING':<10}")
    print("-"*80)
    
    for result in results:
        symbol = result['symbol']
        screener_price = result['metrics']['price']
        binance_price = prices.get(symbol, "N/A")
        signal = result['signal']
        rating = result['rating']
        
        binance_str = f"${binance_price:.2f}" if isinstance(binance_price, (int, float)) else binance_price
        
        print(f"{symbol:<20} ${screener_price:<14.2f} {binance_str:<15} {signal:<15} {rating:<10}")
    
    print("-"*80)
    
    # Step 5: Show actionable signals
    print("\n🎯 ACTIONABLE SIGNALS:")
    print("="*80)
    
    strong_buy = [r for r in results if r['signal'] == 'STRONG_BUY']
    strong_sell = [r for r in results if r['signal'] == 'STRONG_SELL']
    
    if strong_buy:
        print(f"\n🟢 STRONG BUY Signals ({len(strong_buy)}):")
        for r in strong_buy:
            print(f"   • {r['symbol']} - Rating: {r['rating']}")
    
    if strong_sell:
        print(f"\n🔴 STRONG SELL Signals ({len(strong_sell)}):")
        for r in strong_sell:
            print(f"   • {r['symbol']} - Rating: {r['rating']}")
    
    if not strong_buy and not strong_sell:
        print("\n⚪ No strong signals detected. Market is neutral.")
    
    print("\n" + "="*80)
    print("⚠️ DISCLAIMER: This is a demo only. Do not use for real trading without proper testing!")
    print("="*80)


def check_account_demo():
    """
    Demo: Check Binance account balance.
    """
    print("\n\n💼 Binance Account Info Demo")
    print("="*80)
    
    try:
        binance = BinanceIntegration()
        
        print("\n📊 Fetching account balances...")
        balances = binance.get_account_balance()
        
        if balances:
            print(f"\n✅ Account has {len(balances)} assets with non-zero balance:\n")
            print(f"{'ASSET':<10} {'FREE':<15} {'LOCKED':<15} {'TOTAL':<15}")
            print("-"*60)
            
            for asset, bal in balances.items():
                print(f"{asset:<10} {bal['free']:<15.8f} {bal['locked']:<15.8f} {bal['total']:<15.8f}")
        else:
            print("⚠️ No balances found or API error.")
            
    except ImportError:
        print("\n❌ python-binance not installed.")
        print("   Install with: pip install python-binance")
    except ValueError as e:
        print(f"\n⚠️ {e}")
        print("   Set BINANCE_API_KEY and BINANCE_API_SECRET environment variables")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    # Run the main demo
    analyze_and_trade_demo()
    
    # Optionally check account (requires API keys)
    # Uncomment to test:
    # check_account_demo()
