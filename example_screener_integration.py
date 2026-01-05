"""
Example: TradingView Screener Integration with Trading Metrics
Demonstrates how to fetch data from TradingView and analyze with trading_metrics.py
"""

import logging
from tradingview_screener import (
    fetch_screener_indicators,
    fetch_screener_multi_changes,
    map_to_trading_metrics_format,
)
from trading_metrics import compute_metrics
from trading_utils import get_full_analysis, setup_logging


def example_fetch_single_symbols():
    """Example: Fetch specific symbols and analyze"""
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Fetch Specific Symbols")
    print("=" * 60)
    
    symbols = [
        'BINANCE:BTCUSDT',
        'BINANCE:ETHUSDT',
        'BINANCE:BNBUSDT',
    ]
    
    print(f"\nFetching indicators for {len(symbols)} symbols...")
    
    try:
        data = fetch_screener_indicators(
            exchange='binance',
            symbols=symbols,
            timeframe='4h',
            include_extended=True,  # Include MACD, StochRSI, etc.
            validate_data=True,
        )
        
        print(f"✅ Fetched data for {len(data)} symbols\n")
        
        # Analyze each symbol
        for item in data:
            symbol = item['symbol']
            indicators = item['indicators']
            
            print(f"\n{'='*60}")
            print(f"Analyzing: {symbol}")
            print(f"{'='*60}")
            
            # Map to trading metrics format
            formatted = map_to_trading_metrics_format(indicators)
            
            if formatted:
                # Compute trading metrics
                metrics = compute_metrics(formatted)
                
                if metrics:
                    signal = metrics['composite']['signal']
                    rating = metrics['composite']['rating']
                    price = metrics['price']
                    change = metrics['change']
                    
                    print(f"Price: ${price} ({change:+.2f}%)")
                    print(f"Signal: {signal} (Rating: {rating})")
                    print(f"Trend Strength: {metrics['composite']['trend_strength']}")
                else:
                    print(f"❌ Failed to compute metrics for {symbol}")
            else:
                print(f"⚠️ Incomplete indicator data for {symbol}")
                print(f"Available indicators: {list(indicators.keys())}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def example_scan_exchange():
    """Example: Scan entire exchange for opportunities"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Scan Exchange for Top Opportunities")
    print("=" * 60)
    
    print("\nScanning Binance for top 20 pairs...")
    
    try:
        data = fetch_screener_indicators(
            exchange='binance',
            symbols=None,  # Scan mode
            limit=20,
            timeframe='4h',
            include_extended=True,
            validate_data=True,
        )
        
        print(f"✅ Fetched data for {len(data)} symbols\n")
        
        # Analyze and rank by signal strength
        results = []
        
        for item in data:
            symbol = item['symbol']
            indicators = item['indicators']
            
            formatted = map_to_trading_metrics_format(indicators)
            if not formatted:
                continue
            
            metrics = compute_metrics(formatted)
            if not metrics:
                continue
            
            results.append({
                'symbol': symbol,
                'signal': metrics['composite']['signal'],
                'rating': metrics['composite']['rating'],
                'price': metrics['price'],
                'change': metrics['change'],
                'trend_strength': metrics['composite']['trend_strength'],
            })
        
        # Sort by rating (most bullish first)
        results.sort(key=lambda x: x['rating'])
        
        # Display top opportunities
        print("\n🟢 TOP BULLISH OPPORTUNITIES:")
        print("-" * 60)
        bullish = [r for r in results if r['rating'] <= -2][:5]
        if bullish:
            for r in bullish:
                print(f"{r['symbol']:25} | Signal: {r['signal']:12} | "
                      f"Rating: {r['rating']:2} | Price: ${r['price']:.4f} | "
                      f"Change: {r['change']:+.2f}%")
        else:
            print("No strong bullish signals found")
        
        print("\n🔴 TOP BEARISH OPPORTUNITIES:")
        print("-" * 60)
        bearish = [r for r in results if r['rating'] >= 2][:5]
        if bearish:
            for r in bearish:
                print(f"{r['symbol']:25} | Signal: {r['signal']:12} | "
                      f"Rating: {r['rating']:2} | Price: ${r['price']:.4f} | "
                      f"Change: {r['change']:+.2f}%")
        else:
            print("No strong bearish signals found")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def example_multi_timeframe():
    """Example: Multi-timeframe analysis"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Multi-Timeframe Analysis")
    print("=" * 60)
    
    symbols = ['BINANCE:BTCUSDT', 'BINANCE:ETHUSDT']
    timeframes = ['15m', '1h', '4h', '1D']
    
    print(f"\nFetching multi-timeframe data for {len(symbols)} symbols...")
    print(f"Timeframes: {', '.join(timeframes)}\n")
    
    try:
        data = fetch_screener_multi_changes(
            exchange='binance',
            symbols=symbols,
            timeframes=timeframes,
            base_timeframe='4h',
            validate_data=True,
        )
        
        for item in data:
            symbol = item['symbol']
            changes = item['changes']
            base_indicators = item['base_indicators']
            
            print(f"\n{'='*60}")
            print(f"{symbol}")
            print(f"{'='*60}")
            
            # Display changes across timeframes
            print("\n📊 Price Changes:")
            for tf in timeframes:
                change = changes.get(tf)
                if change is not None:
                    emoji = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
                    print(f"  {tf:4} : {emoji} {change:+.2f}%")
                else:
                    print(f"  {tf:4} : ⚠️ No data")
            
            # Analyze base timeframe
            print(f"\n📈 Base Timeframe (4h) Analysis:")
            print(f"  Price: ${base_indicators['close']:.4f}")
            print(f"  BB Upper: ${base_indicators['BB.upper']:.4f}")
            print(f"  BB Middle: ${base_indicators['SMA20']:.4f}")
            print(f"  BB Lower: ${base_indicators['BB.lower']:.4f}")
            print(f"  Volume: {base_indicators['volume']:,.0f}")
            
            # Determine trend alignment
            bullish_tfs = sum(1 for c in changes.values() if c and c > 0)
            bearish_tfs = sum(1 for c in changes.values() if c and c < 0)
            
            print(f"\n🎯 Trend Alignment:")
            print(f"  Bullish timeframes: {bullish_tfs}/{len(timeframes)}")
            print(f"  Bearish timeframes: {bearish_tfs}/{len(timeframes)}")
            
            if bullish_tfs >= 3:
                print(f"  ✅ Strong bullish alignment")
            elif bearish_tfs >= 3:
                print(f"  ⚠️ Strong bearish alignment")
            else:
                print(f"  ➡️ Mixed signals")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def example_full_analysis():
    """Example: Complete analysis with detailed output"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Full Detailed Analysis")
    print("=" * 60)
    
    symbol = 'BINANCE:BTCUSDT'
    
    print(f"\nFetching complete analysis for {symbol}...\n")
    
    try:
        data = fetch_screener_indicators(
            exchange='binance',
            symbols=[symbol],
            timeframe='4h',
            include_extended=True,
            validate_data=True,
        )
        
        if not data:
            print(f"❌ No data returned for {symbol}")
            return
        
        item = data[0]
        indicators = item['indicators']
        
        # Map to trading metrics format
        formatted = map_to_trading_metrics_format(indicators)
        
        if not formatted:
            print(f"⚠️ Incomplete indicator data")
            print(f"Available: {list(indicators.keys())}")
            return
        
        # Compute metrics
        metrics = compute_metrics(formatted)
        
        if metrics:
            # Display full analysis
            print(get_full_analysis(metrics))
        else:
            print(f"❌ Failed to compute metrics")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all examples"""
    # Setup logging
    setup_logging(level=logging.INFO)
    
    print("\n" + "=" * 60)
    print("TRADINGVIEW SCREENER + TRADING METRICS INTEGRATION")
    print("=" * 60)
    print("\n⚠️ IMPORTANT NOTES:")
    print("  • Extended indicators (MACD, StochRSI, ADX, CCI) require")
    print("    verification of TradingView column names")
    print("  • Set include_extended=True to fetch all indicators")
    print("  • Some examples may fail if column names don't match")
    print("  • Check logs for detailed error messages")
    print("\n")
    
    try:
        # Run examples
        example_fetch_single_symbols()
        example_scan_exchange()
        example_multi_timeframe()
        example_full_analysis()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("EXAMPLES COMPLETE")
    print("=" * 60)
    print("\n💡 Next Steps:")
    print("  1. Verify TradingView column names for extended indicators")
    print("  2. Update EXTENDED_INDICATORS in tradingview_screener.py")
    print("  3. Test with your exchange and symbols")
    print("  4. Integrate into your trading bot")
    print("\n")


if __name__ == "__main__":
    main()
