#!/usr/bin/env python3
"""
Automated Trading Analysis Script

This script is designed to run periodically (e.g., via cron or Task Scheduler)
to continuously monitor cryptocurrency markets and generate trading signals.

Usage:
    # Run once
    python automated_analysis.py

    # Run with custom config
    python automated_analysis.py --exchange BINANCE --timeframe 4h --symbols BTCUSDT,ETHUSDT

    # Run with filters
    python automated_analysis.py --min-signal STRONG_BUY --notify

Scheduling Examples:

    Windows Task Scheduler:
        Program: C:\path\to\python.exe
        Arguments: C:\path\to\automated_analysis.py
        Trigger: Daily at 9:00 AM

    Linux/Mac Cron:
        # Run every 4 hours
        0 */4 * * * /usr/bin/python3 /path/to/automated_analysis.py

        # Run every day at 9 AM
        0 9 * * * /usr/bin/python3 /path/to/automated_analysis.py
"""

import argparse
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from pathlib import Path

# Import our modules
from tradingview_screener import (
    fetch_screener_indicators,
    map_to_trading_metrics_format,
    validate_indicator_data
)
from trading_metrics import compute_metrics
from trading_utils import get_full_analysis, setup_logging
from trading_constants import Signal


# Configuration
DEFAULT_SYMBOLS = [
    # Major cryptocurrencies
    'BTCUSDT', 'ETHUSDT', 'BNBUSDT',
    # Large caps
    'SOLUSDT', 'XRPUSDT', 'ADAUSDT', 'DOGEUSDT',
    # Mid caps
    'MATICUSDT', 'LINKUSDT', 'AVAXUSDT', 'UNIUSDT',
    # Small caps
    'ATOMUSDT', 'DOTUSDT', 'NEARUSDT', 'ALGOUSDT'
]

DEFAULT_EXCHANGE = 'BINANCE'
DEFAULT_TIMEFRAME = '1h'
OUTPUT_DIR = Path('analysis_reports')
ALERT_SIGNALS = [Signal.STRONG_BUY, Signal.STRONG_SELL]


def setup_argparse() -> argparse.ArgumentParser:
    """Setup command-line argument parser"""
    parser = argparse.ArgumentParser(
        description='Automated Cryptocurrency Trading Analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--symbols',
        type=str,
        help='Comma-separated list of symbols (e.g., BTCUSDT,ETHUSDT). Default: major cryptos'
    )

    parser.add_argument(
        '--exchange',
        type=str,
        default=DEFAULT_EXCHANGE,
        help=f'Exchange name (default: {DEFAULT_EXCHANGE})'
    )

    parser.add_argument(
        '--timeframe',
        type=str,
        default=DEFAULT_TIMEFRAME,
        choices=['5m', '15m', '1h', '4h', '1D', '1W', '1M'],
        help=f'Analysis timeframe (default: {DEFAULT_TIMEFRAME})'
    )

    parser.add_argument(
        '--min-signal',
        type=str,
        choices=['STRONG_BUY', 'BUY', 'NEUTRAL', 'SELL', 'STRONG_SELL'],
        help='Only report signals at or above this level'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default=str(OUTPUT_DIR),
        help=f'Output directory for reports (default: {OUTPUT_DIR})'
    )

    parser.add_argument(
        '--notify',
        action='store_true',
        help='Create notification file for strong signals (for external scripts to read)'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Also output results in JSON format'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress console output (only log to file)'
    )

    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level (default: INFO)'
    )

    return parser


def filter_by_signal(
    results: Dict[str, Dict[str, Any]],
    min_signal: Optional[str]
) -> Dict[str, Dict[str, Any]]:
    """
    Filter results by minimum signal strength

    Args:
        results: Analysis results
        min_signal: Minimum signal level to include

    Returns:
        Filtered results
    """
    if not min_signal:
        return results

    signal_order = {
        'STRONG_SELL': 0,
        'SELL': 1,
        'NEUTRAL': 2,
        'BUY': 3,
        'STRONG_BUY': 4
    }

    min_level = signal_order[min_signal]
    filtered = {}

    for symbol, data in results.items():
        signal = data['composite_signal']
        if signal_order[signal] >= min_level:
            filtered[symbol] = data

    return filtered


def save_report(
    results: Dict[str, Dict[str, Any]],
    output_dir: Path,
    timeframe: str,
    exchange: str,
    as_json: bool = False
) -> tuple[str, Optional[str]]:
    """
    Save analysis report to file

    Args:
        results: Analysis results
        output_dir: Output directory
        timeframe: Analysis timeframe
        exchange: Exchange name
        as_json: Also save as JSON

    Returns:
        Tuple of (text_report_path, json_report_path)
    """
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
    base_name = f'automated-analysis-{timestamp}'

    # Save text report
    txt_path = output_dir / f'{base_name}.txt'
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("AUTOMATED CRYPTOCURRENCY TRADING ANALYSIS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Timeframe: {timeframe}\n")
        f.write(f"Exchange: {exchange}\n")
        f.write(f"Symbols Analyzed: {len(results)}\n\n")

        # Group by signal
        by_signal = {}
        for symbol, data in results.items():
            signal = data['composite_signal']
            if signal not in by_signal:
                by_signal[signal] = []
            by_signal[signal].append((symbol, data))

        # Write summary
        f.write("SUMMARY\n")
        f.write("-" * 80 + "\n\n")
        signal_order = ['STRONG_BUY', 'BUY', 'NEUTRAL', 'SELL', 'STRONG_SELL']
        for signal in signal_order:
            if signal in by_signal:
                f.write(f"{signal}: {len(by_signal[signal])} symbols\n")

        # Write detailed results
        f.write("\n\nDETAILED ANALYSIS\n")
        f.write("=" * 80 + "\n\n")

        for signal in signal_order:
            if signal in by_signal:
                f.write(f"\n{signal} SIGNALS ({len(by_signal[signal])} symbols)\n")
                f.write("-" * 80 + "\n\n")

                for symbol, data in by_signal[signal]:
                    f.write(f"\n{'='*80}\n")
                    f.write(f"{symbol}\n")
                    f.write(f"{'='*80}\n")
                    f.write(data['analysis'])
                    f.write(f"\n{'='*80}\n\n")

    # Save JSON report if requested
    json_path = None
    if as_json:
        json_path = output_dir / f'{base_name}.json'

        # Prepare JSON-serializable data
        json_data = {
            'timestamp': datetime.now().isoformat(),
            'timeframe': timeframe,
            'exchange': exchange,
            'symbols_analyzed': len(results),
            'results': {}
        }

        for symbol, data in results.items():
            json_data['results'][symbol] = {
                'signal': data['composite_signal'],
                'recommendation': data['recommendation'],
                'metrics': data['metrics'],
                'indicators': {
                    k: float(v) if isinstance(v, (int, float)) else v
                    for k, v in data['indicators'].items()
                }
            }

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2)

    return str(txt_path), str(json_path) if json_path else None


def create_notification_file(
    results: Dict[str, Dict[str, Any]],
    output_dir: Path
) -> Optional[str]:
    """
    Create notification file for strong signals

    This file can be read by external scripts (e.g., Telegram bot)
    to send alerts

    Args:
        results: Analysis results
        output_dir: Output directory

    Returns:
        Path to notification file or None
    """
    # Filter for strong signals
    alerts = {}
    for symbol, data in results.items():
        signal = data['composite_signal']
        if signal in ['STRONG_BUY', 'STRONG_SELL']:
            alerts[symbol] = {
                'signal': signal,
                'recommendation': data['recommendation'],
                'timestamp': datetime.now().isoformat()
            }

    if not alerts:
        return None

    # Create notification file
    output_dir.mkdir(parents=True, exist_ok=True)
    notify_path = output_dir / 'ALERTS.json'

    with open(notify_path, 'w', encoding='utf-8') as f:
        json.dump(alerts, f, indent=2)

    return str(notify_path)


def main():
    """Main execution function"""
    # Parse arguments
    parser = setup_argparse()
    args = parser.parse_args()

    # Setup logging
    log_level = 'ERROR' if args.quiet else args.log_level
    setup_logging(
        log_file='automated_analysis.log',
        console_level=log_level
    )
    logger = logging.getLogger(__name__)

    logger.info("="*80)
    logger.info("AUTOMATED TRADING ANALYSIS STARTED")
    logger.info("="*80)

    # Parse symbols
    if args.symbols:
        symbols = [s.strip().upper() for s in args.symbols.split(',')]
    else:
        symbols = DEFAULT_SYMBOLS

    logger.info(f"Analyzing {len(symbols)} symbols on {args.exchange} ({args.timeframe})")

    try:
        # Fetch data from TradingView
        logger.info("Fetching data from TradingView...")
        screener_data = fetch_screener_indicators(
            symbols=symbols,
            exchange=args.exchange,
            timeframe=args.timeframe,
            include_extended=True
        )

        if not screener_data:
            logger.error("No data fetched from TradingView")
            return 1

        logger.info(f"Fetched data for {len(screener_data)} symbols")

        # Analyze each symbol
        results = {}
        for data in screener_data:
            symbol = data.get('symbol', 'UNKNOWN')

            try:
                # Convert and validate
                indicators = map_to_trading_metrics_format(data)
                if not validate_indicator_data(indicators, symbol):
                    continue

                # Compute metrics
                metrics = compute_metrics(indicators)
                if not metrics:
                    continue

                # Get analysis
                analysis = get_full_analysis(indicators, metrics, symbol)

                results[symbol] = {
                    'indicators': indicators,
                    'metrics': metrics,
                    'analysis': analysis,
                    'composite_signal': metrics['composite_signal'],
                    'recommendation': analysis.split('\n')[0]
                }

                logger.info(f"{symbol}: {metrics['composite_signal']}")

            except Exception as e:
                logger.error(f"{symbol}: Analysis error: {e}", exc_info=True)
                continue

        # Filter by minimum signal if specified
        if args.min_signal:
            original_count = len(results)
            results = filter_by_signal(results, args.min_signal)
            logger.info(f"Filtered: {original_count} → {len(results)} symbols (min: {args.min_signal})")

        # Save reports
        output_dir = Path(args.output_dir)
        txt_path, json_path = save_report(
            results,
            output_dir,
            args.timeframe,
            args.exchange,
            as_json=args.json
        )

        logger.info(f"✅ Text report saved: {txt_path}")
        if json_path:
            logger.info(f"✅ JSON report saved: {json_path}")

        # Create notification file if requested
        if args.notify:
            notify_path = create_notification_file(results, output_dir)
            if notify_path:
                logger.info(f"🔔 Alerts file created: {notify_path}")
            else:
                logger.info("No strong signals to notify")

        # Print summary to console if not quiet
        if not args.quiet:
            print("\n" + "="*80)
            print("ANALYSIS COMPLETE")
            print("="*80)
            print(f"\nAnalyzed: {len(results)} symbols")
            print(f"Report: {txt_path}")
            if json_path:
                print(f"JSON: {json_path}")

            # Quick summary
            by_signal = {}
            for data in results.values():
                signal = data['composite_signal']
                by_signal[signal] = by_signal.get(signal, 0) + 1

            print("\nSignal Distribution:")
            for signal in ['STRONG_BUY', 'BUY', 'NEUTRAL', 'SELL', 'STRONG_SELL']:
                if signal in by_signal:
                    print(f"  {signal:15s}: {by_signal[signal]} symbols")

            print("\n" + "="*80 + "\n")

        logger.info("="*80)
        logger.info("AUTOMATED TRADING ANALYSIS COMPLETED SUCCESSFULLY")
        logger.info("="*80)

        return 0

    except KeyboardInterrupt:
        logger.info("Analysis interrupted by user")
        return 130

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        if not args.quiet:
            print(f"\n❌ Error: {e}")
            print("Check automated_analysis.log for details")
        return 1


if __name__ == '__main__':
    exit(main())
