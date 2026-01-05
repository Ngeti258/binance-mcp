#!/usr/bin/env python3
"""
Quick Start Script - Complete Trading System Demo
This script demonstrates the full system working end-to-end:
1. Fetches data from TradingView
2. Computes trading metrics
3. Generates analysis and recommendations
"""

import logging
from typing import List, Dict, Any
from datetime import datetime

# Import our modules
from tradingview_screener import (
    fetch_screener_indicators,
    map_to_trading_metrics_format,
    validate_indicator_data
)
from trading_metrics import compute_metrics
from trading_utils import get_full_analysis, setup_logging

# Setup logging
setup_logging(log_file='quick_start.log', console_level='INFO')
logger = logging.getLogger(__name__)


def analyze_symbols(
    symbols: List[str],
    exchange: str = 'BINANCE',
    timeframe: str = '1h'
) -> Dict[str, Dict[str, Any]]:
    """
    Analyze a list of cryptocurrency symbols

    Args:
        symbols: List of trading symbols (e.g., ['BTCUSD', 'ETHUSD'])
        exchange: Exchange name (default: 'BINANCE')
        timeframe: Analysis timeframe (default: '1h')

    Returns:
        Dictionary mapping symbols to their analysis results
    """
    logger.info(f"Analyzing {len(symbols)} symbols on {exchange} ({timeframe})")
    logger.info(f"Symbols: {', '.join(symbols)}")

    # Fetch data from TradingView
    logger.info("Fetching data from TradingView...")
    screener_data = fetch_screener_indicators(
        symbols=symbols,
        exchange=exchange,
        timeframe=timeframe,
        include_extended=True  # Get all indicators including MACD, StochRSI, ADX, CCI
    )

    if not screener_data:
        logger.error("No data fetched from TradingView")
        return {}

    logger.info(f"Fetched data for {len(screener_data)} symbols")

    # Analyze each symbol
    results = {}
    for data in screener_data:
        symbol = data.get('symbol', 'UNKNOWN')

        try:
            # Convert to trading metrics format
            indicators = map_to_trading_metrics_format(data)

            # Validate data
            if not validate_indicator_data(indicators, symbol):
                logger.warning(f"{symbol}: Skipping due to validation failure")
                continue

            # Compute metrics
            metrics = compute_metrics(indicators)
            if not metrics:
                logger.warning(f"{symbol}: Failed to compute metrics")
                continue

            # Get full analysis
            analysis = get_full_analysis(
                indicators=indicators,
                metrics=metrics,
                symbol=symbol
            )

            results[symbol] = {
                'indicators': indicators,
                'metrics': metrics,
                'analysis': analysis,
                'composite_signal': metrics['composite_signal'],
                'recommendation': analysis.split('\n')[0]  # First line has the recommendation
            }

            logger.info(f"{symbol}: {metrics['composite_signal']} - {results[symbol]['recommendation']}")

        except Exception as e:
            logger.error(f"{symbol}: Error during analysis: {e}", exc_info=True)
            continue

    return results


def print_summary(results: Dict[str, Dict[str, Any]]) -> None:
    """Print a summary of analysis results"""
    print("\n" + "="*80)
    print("TRADING ANALYSIS SUMMARY")
    print("="*80 + "\n")

    if not results:
        print("No results to display")
        return

    # Group by signal
    by_signal = {}
    for symbol, data in results.items():
        signal = data['composite_signal']
        if signal not in by_signal:
            by_signal[signal] = []
        by_signal[signal].append(symbol)

    # Print grouped results
    signal_order = ['STRONG_BUY', 'BUY', 'NEUTRAL', 'SELL', 'STRONG_SELL']
    for signal in signal_order:
        if signal in by_signal:
            symbols = by_signal[signal]
            print(f"\n{signal} ({len(symbols)} symbols):")
            print("-" * 40)
            for symbol in symbols:
                rec = results[symbol]['recommendation']
                print(f"  {symbol:15s} - {rec}")

    print("\n" + "="*80)
    print(f"Analyzed {len(results)} symbols at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")


def print_detailed_analysis(symbol: str, result: Dict[str, Any]) -> None:
    """Print detailed analysis for a specific symbol"""
    print("\n" + "="*80)
    print(f"DETAILED ANALYSIS: {symbol}")
    print("="*80)
    print(result['analysis'])
    print("="*80 + "\n")


def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("CRYPTOCURRENCY TRADING SYSTEM - QUICK START")
    print("="*80 + "\n")

    # Define symbols to analyze (major cryptocurrencies)
    major_symbols = [
        'BTCUSDT',   # Bitcoin
        'ETHUSDT',   # Ethereum
        'BNBUSDT',   # Binance Coin
        'SOLUSDT',   # Solana
        'XRPUSDT',   # Ripple
        'ADAUSDT',   # Cardano
        'DOGEUSDT',  # Dogecoin
        'MATICUSDT', # Polygon
    ]

    # Analyze on 1-hour timeframe
    results = analyze_symbols(
        symbols=major_symbols,
        exchange='BINANCE',
        timeframe='1h'
    )

    # Print summary
    print_summary(results)

    # Print detailed analysis for first symbol with STRONG_BUY or STRONG_SELL
    for symbol, data in results.items():
        signal = data['composite_signal']
        if signal in ['STRONG_BUY', 'STRONG_SELL']:
            print_detailed_analysis(symbol, data)
            break

    # Save results to file
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
    output_file = f'quick-start-analysis-{timestamp}.txt'

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("CRYPTOCURRENCY TRADING ANALYSIS\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Timeframe: 1h\n")
            f.write(f"Exchange: BINANCE\n\n")

            for symbol, data in results.items():
                f.write(f"\n{'='*80}\n")
                f.write(f"{symbol}\n")
                f.write(f"{'='*80}\n")
                f.write(data['analysis'])
                f.write(f"\n{'='*80}\n\n")

        print(f"✅ Full analysis saved to: {output_file}")
        print(f"✅ Logs saved to: quick_start.log\n")

    except Exception as e:
        logger.error(f"Failed to save results: {e}", exc_info=True)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user")
        logger.info("Analysis interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        print("Check quick_start.log for details")
