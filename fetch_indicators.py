"""
Quick script to fetch TradingView indicators for remaining major cryptocurrencies
"""
import json
import logging
from tradingview_screener_local import fetch_screener_indicators

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Define coins to fetch
COINS = [
    'BINANCE:UNIUSD',
    'BINANCE:ATOMUSD',
    'BINANCE:LTCUSD',
    'BINANCE:TRXUSD',
    'BINANCE:DOGEUSD',
    'BINANCE:MATICUSD'
]

def main():
    """Fetch indicators for all coins"""
    results = {}

    for symbol in COINS:
        coin_name = symbol.split(':')[1]
        logger.info(f"\nFetching indicators for {coin_name}...")

        try:
            # Fetch data
            data = fetch_screener_indicators(
                exchange='BINANCE',
                symbols=[symbol],
                timeframe='1h',
                include_extended=True,
                validate_data=True
            )

            if data and len(data) > 0:
                indicators = data[0]['indicators']
                results[coin_name] = {
                    'success': True,
                    'symbol': symbol,
                    'indicators': indicators
                }
                logger.info(f"✓ Successfully fetched {coin_name}")
                logger.info(f"  Close: ${indicators.get('close', 'N/A')}")
                logger.info(f"  RSI: {indicators.get('RSI', 'N/A')}")
            else:
                results[coin_name] = {
                    'success': False,
                    'symbol': symbol,
                    'error': 'No data returned'
                }
                logger.warning(f"✗ No data for {coin_name}")

        except Exception as e:
            results[coin_name] = {
                'success': False,
                'symbol': symbol,
                'error': str(e)
            }
            logger.error(f"✗ Error fetching {coin_name}: {e}")

    # Print summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    successful = sum(1 for r in results.values() if r['success'])
    print(f"\nSuccessfully fetched: {successful}/{len(COINS)} coins\n")

    # Print full results as JSON
    print("\n" + "="*80)
    print("FULL RESULTS (JSON)")
    print("="*80 + "\n")
    print(json.dumps(results, indent=2, default=str))

    return results

if __name__ == '__main__':
    main()
