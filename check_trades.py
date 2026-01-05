#!/usr/bin/env python3
"""
Quick Paper Trading Position Monitor - FULLY AUTOMATED
Checks open positions against live Binance prices
Auto-closes positions when stop loss or targets are hit
Optimized for frequent execution (every 15-30 minutes)

NO USER INPUT REQUIRED - Runs completely automatically
"""

import sys
import os
import json
import requests
from datetime import datetime
from pathlib import Path

# Add project to path
sys.path.append(str(Path(__file__).parent))

from paper_trading_db import PaperTradingDB

# Try to import pytz, fall back to manual offset if not available
try:
    import pytz
    EAT = pytz.timezone('Africa/Nairobi')
    def get_nairobi_time():
        return datetime.now(EAT)
except ImportError:
    from datetime import timezone, timedelta
    EAT_OFFSET = timezone(timedelta(hours=3))
    def get_nairobi_time():
        return datetime.now(EAT_OFFSET)

# Binance API endpoint
BINANCE_API_BASE = "https://api.binance.com/api/v3"

# USD to KES rate (update periodically)
USD_TO_KES = 129.50

def get_current_prices_from_binance(symbols):
    """
    Fetch current prices directly from Binance REST API
    No authentication required for public market data
    """
    prices = {}

    try:
        # Fetch all ticker prices in one call
        response = requests.get(f"{BINANCE_API_BASE}/ticker/price", timeout=10)
        response.raise_for_status()

        all_prices = response.json()

        # Create lookup dictionary
        price_lookup = {item['symbol']: float(item['price']) for item in all_prices}

        # Get prices for our symbols
        for symbol in symbols:
            if symbol in price_lookup:
                prices[symbol] = price_lookup[symbol]
            else:
                print(f"Warning: {symbol} not found in Binance data")

        return prices

    except requests.exceptions.RequestException as e:
        print(f"Error fetching prices from Binance: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing Binance response: {e}")
        return None

def get_usd_to_kes_rate():
    """
    Get current USD to KES exchange rate
    Falls back to default if API fails
    """
    try:
        # Try exchangerate-api (free tier)
        response = requests.get(
            "https://api.exchangerate-api.com/v4/latest/USD",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('rates', {}).get('KES', USD_TO_KES)
    except:
        pass

    return USD_TO_KES

def format_pnl(pnl_percent):
    """Format P&L with sign"""
    if pnl_percent > 0:
        return f"+{pnl_percent:.2f}%"
    else:
        return f"{pnl_percent:.2f}%"

def get_status_action(old_status, new_status, side):
    """Get action description based on status change"""
    if new_status == 'STOPPED':
        return "[CLOSED - Stop Loss Hit]"
    elif new_status == 'TP2_HIT':
        return "[CLOSED - Target 2 Hit]"
    elif new_status == 'TP1_HIT' and old_status == 'OPEN':
        return "[Target 1 Reached]"
    elif new_status in ('OPEN', 'TP1_HIT'):
        return "[Monitoring]"
    else:
        return f"[{new_status}]"

def check_trades_automated():
    """
    Main automated function - NO USER INPUT REQUIRED
    Fetches prices from Binance and updates all positions
    """
    db = PaperTradingDB()
    now = get_nairobi_time()

    # Get USD to KES rate
    usd_to_kes = get_usd_to_kes_rate()

    print("\n" + "=" * 80)
    print("=== PAPER TRADING POSITION CHECK ===")
    print(f"Timestamp: {now.strftime('%Y-%m-%d %H:%M:%S')} EAT")
    print(f"Auto-Close: ENABLED")
    print(f"USD/KES Rate: {usd_to_kes:.2f}")
    print("=" * 80)

    # Get open positions
    open_trades = db.get_open_trades()

    if not open_trades:
        print("\nNo open positions.\n")
        log_check(now, 0, 0, [], usd_to_kes)
        return

    # Get unique symbols
    symbols = list(set(trade['symbol'] for trade in open_trades))

    print(f"\nFetching prices for {len(symbols)} symbols from Binance...")

    # Fetch current prices from Binance
    current_prices = get_current_prices_from_binance(symbols)

    if current_prices is None:
        print("ERROR: Could not fetch prices from Binance. Skipping check.")
        return

    print(f"Prices fetched successfully.\n")

    # Display header
    print(f"POSITION STATUS ({len(open_trades)} trades checked)\n")
    print(f"{'Symbol':<12} {'Side':<6} {'Entry':<12} {'Current':<12} {'P&L%':<10} {'Status':<12} {'Action'}")
    print("-" * 90)

    # Track results
    closed_trades = []
    still_open = []
    alerts = []
    portfolio_pnl_usd = 0

    for trade in open_trades:
        symbol = trade['symbol']
        side = trade['side']
        entry = trade['entry_price_usd']
        old_status = trade['status']
        position_size = trade['position_size_usd']

        # Get current price
        current_price = current_prices.get(symbol)
        if current_price is None:
            print(f"{symbol:<12} {side:<6} - ERROR: No price data")
            continue

        # Update trade check in database (this handles auto-close)
        result = db.update_trade_check(
            trade['trade_id'],
            current_price,
            current_price * usd_to_kes
        )

        # Get results
        unrealized_pnl = result.get('unrealized_pnl_percent', 0)
        new_status = result.get('status', old_status)

        # Calculate P&L in USD
        pnl_usd = position_size * (unrealized_pnl / 100)

        # Get action description
        action = get_status_action(old_status, new_status, side)

        # Format output
        pnl_str = format_pnl(unrealized_pnl)

        print(f"{symbol:<12} {side:<6} ${entry:<11,.2f} ${current_price:<11,.2f} {pnl_str:<10} {new_status:<12} {action}")

        # Track closed vs open
        if new_status in ('STOPPED', 'TP2_HIT', 'CLOSED'):
            closed_trades.append({
                'symbol': symbol,
                'side': side,
                'pnl_percent': unrealized_pnl,
                'pnl_usd': pnl_usd,
                'reason': 'Stop Loss' if new_status == 'STOPPED' else 'Target 2'
            })
        else:
            still_open.append(trade)
            portfolio_pnl_usd += pnl_usd

        # Generate alerts
        if new_status == 'STOPPED' and old_status != 'STOPPED':
            alerts.append(f"CRITICAL: {symbol} {side} STOPPED at ${current_price:.2f} ({pnl_str})")
        elif new_status == 'TP2_HIT' and old_status != 'TP2_HIT':
            alerts.append(f"SUCCESS: {symbol} {side} TP2 HIT at ${current_price:.2f} ({pnl_str})")
        elif new_status == 'TP1_HIT' and old_status == 'OPEN':
            alerts.append(f"INFO: {symbol} {side} TP1 HIT at ${current_price:.2f} - Consider trailing stop")
        elif abs(unrealized_pnl) > 2 and new_status in ('OPEN', 'TP1_HIT'):
            alerts.append(f"WARNING: {symbol} {side} Large move: {pnl_str}")

    print("-" * 90)

    # Summary section
    if closed_trades:
        print(f"\nCLOSED THIS CHECK: {len(closed_trades)} positions")
        for ct in closed_trades:
            pnl_sign = '+' if ct['pnl_usd'] >= 0 else ''
            print(f"  - {ct['symbol']} {ct['side']}: {format_pnl(ct['pnl_percent'])} (${pnl_sign}{ct['pnl_usd']:.2f}) - {ct['reason']}")

    print(f"\nSTILL OPEN: {len(still_open)} positions")

    # Portfolio summary
    portfolio_pnl_kes = portfolio_pnl_usd * usd_to_kes
    avg_pnl_percent = (portfolio_pnl_usd / (len(still_open) * 1000)) * 100 if still_open else 0

    print(f"Portfolio Unrealized P&L: ${portfolio_pnl_usd:+,.2f} (KSh {portfolio_pnl_kes:+,.2f}) | {format_pnl(avg_pnl_percent)}")

    # Alerts
    if alerts:
        print(f"\n{'='*80}")
        print(f"ALERTS ({len(alerts)}):")
        for alert in alerts:
            print(f"  {alert}")

    print(f"\nNext check recommended: 15-30 minutes")
    print("=" * 80 + "\n")

    # Log to file
    log_check(now, len(open_trades), portfolio_pnl_usd, alerts, usd_to_kes, closed_trades)

def log_check(timestamp, position_count, portfolio_pnl, alerts, usd_to_kes, closed_trades=None):
    """Log check results to file"""
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "trade_checks.log"

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Check Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')} EAT\n")
        f.write(f"Open Positions: {position_count}\n")
        f.write(f"Portfolio P&L: ${portfolio_pnl:+,.2f}\n")
        f.write(f"USD/KES Rate: {usd_to_kes:.2f}\n")

        if closed_trades:
            f.write(f"Positions Closed: {len(closed_trades)}\n")
            for ct in closed_trades:
                f.write(f"  - {ct['symbol']} {ct['side']}: {ct['reason']}\n")

        if alerts:
            f.write(f"Alerts: {len(alerts)}\n")
            for alert in alerts:
                f.write(f"  {alert}\n")
        else:
            f.write("Alerts: None\n")

        f.write(f"{'='*60}\n")

if __name__ == "__main__":
    """
    Run automated trade check
    No user input required - fetches data directly from Binance
    """
    check_trades_automated()
