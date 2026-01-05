#!/usr/bin/env python3
"""
Daily Paper Trading Review - FULLY AUTOMATED
Analyzes closed trades, calculates performance metrics, identifies patterns
NO USER INPUT REQUIRED
"""

import sys
import io
from pathlib import Path
from datetime import datetime, timedelta

# Set stdout to use utf-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.append(str(Path(__file__).parent))

from paper_trading_db import PaperTradingDB

# Try to import pytz, fall back to manual offset
try:
    import pytz
    EAT = pytz.timezone('Africa/Nairobi')
    def get_nairobi_time():
        return datetime.now(EAT)
except ImportError:
    from datetime import timezone
    EAT_OFFSET = timezone(timedelta(hours=3))
    EAT = None
    def get_nairobi_time():
        return datetime.now(EAT_OFFSET)

def daily_review():
    """Generate daily performance review - FULLY AUTOMATED"""
    db = PaperTradingDB()
    now = get_nairobi_time()

    print("\n" + "="*80)
    print("=== DAILY PAPER TRADING REVIEW ===")
    print(f"Date: {now.strftime('%Y-%m-%d %A')}")
    print(f"Time: {now.strftime('%H:%M:%S')} EAT")
    print("="*80 + "\n")

    # Get overall stats
    stats = db.get_strategy_stats()

    if not stats or stats['total_trades'] == 0:
        print("No closed trades yet. Keep monitoring your open positions!\n")
        # Still save a log file
        save_log(now, None, [], [])
        return

    print("PERFORMANCE SUMMARY")
    print("-" * 80)
    print(f"Total Trades Closed: {stats['total_trades']}")
    print(f"Wins: {stats['wins']} | Losses: {stats['losses']}")
    print(f"Win Rate: {stats['win_rate']:.1f}%")
    print(f"")
    print(f"Total P&L: ${stats['total_pnl_usd']:.2f} USD (KSh {stats['total_pnl_usd'] * 129.50:,.2f})")
    print(f"Average P&L per Trade: {stats['avg_pnl_percent']:.2f}%")
    print(f"")
    print(f"Best Trade: {stats['best_trade_percent']:.2f}%")
    print(f"Worst Trade: {stats['worst_trade_percent']:.2f}%")
    print(f"Average Win: {stats['avg_win_percent']:.2f}%" if stats['avg_win_percent'] else "Average Win: N/A")
    print(f"Average Loss: {stats['avg_loss_percent']:.2f}%" if stats['avg_loss_percent'] else "Average Loss: N/A")
    print("-" * 80 + "\n")

    # Get recent closed trades (last 24 hours)
    recent_trades = db.get_trade_history(limit=20)
    yesterday = now - timedelta(days=1)

    today_trades = []
    for t in recent_trades:
        if t['exit_time']:
            try:
                exit_dt = datetime.fromisoformat(t['exit_time'].replace('Z', '+00:00'))
                if EAT:
                    exit_dt = exit_dt.astimezone(EAT)
                if exit_dt >= yesterday:
                    today_trades.append(t)
            except:
                pass

    if today_trades:
        print(f"TRADES CLOSED TODAY ({len(today_trades)})")
        print("-" * 80)

        for trade in today_trades:
            symbol = trade['symbol']
            side = trade['side']
            entry = trade['entry_price_usd']
            exit_price = trade['exit_price_usd']
            pnl_pct = trade['pnl_percent']
            pnl_usd = trade['pnl_usd']
            exit_reason = trade['exit_reason']

            pnl_str = f"+{pnl_pct:.2f}%" if pnl_pct > 0 else f"{pnl_pct:.2f}%"
            status_icon = "[WIN]" if pnl_pct > 0 else "[LOSS]"

            print(f"{status_icon} {symbol} {side}")
            print(f"   Entry: ${entry:.2f} -> Exit: ${exit_price:.2f}")
            print(f"   P&L: {pnl_str} (${pnl_usd:.2f} USD)")
            print(f"   Exit Reason: {exit_reason}")
            print(f"   Rationale: {trade.get('rationale', 'N/A')}")
            print()

        print("-" * 80 + "\n")

    # Get open positions
    open_trades = db.get_open_trades()

    print(f"OPEN POSITIONS ({len(open_trades)} trades)")
    print("-" * 80)

    if open_trades:
        for trade in open_trades:
            symbol = trade['symbol']
            side = trade['side']
            entry = trade['entry_price_usd']
            status = trade['status']

            print(f"[OPEN] {symbol} {side} @ ${entry:.2f} - Status: {status}")

        print()
    else:
        print("No open positions.\n")

    print("-" * 80)

    # Key insights
    print("\nKEY INSIGHTS")
    print("-" * 80)

    if stats['win_rate'] >= 60:
        print("[OK] Strong win rate! Keep following your strategy.")
    elif stats['win_rate'] >= 50:
        print("[!] Win rate is positive but can improve. Review losing trades for patterns.")
    else:
        print("[X] Win rate below 50%. Consider adjusting strategy or risk management.")

    if stats['avg_win_percent'] and stats['avg_loss_percent']:
        win_loss_ratio = abs(stats['avg_win_percent'] / stats['avg_loss_percent'])
        if win_loss_ratio >= 2:
            print(f"[OK] Excellent risk/reward ratio: {win_loss_ratio:.1f}:1")
        elif win_loss_ratio >= 1.5:
            print(f"[!] Decent risk/reward ratio: {win_loss_ratio:.1f}:1. Aim for 2:1+")
        else:
            print(f"[X] Poor risk/reward ratio: {win_loss_ratio:.1f}:1. Cut losses faster!")

    print("-" * 80 + "\n")

    # Save log file
    save_log(now, stats, today_trades, open_trades)

    print("\n" + "="*80 + "\n")

def save_log(now, stats, today_trades, open_trades):
    """Save daily review to log file"""
    log_dir = Path(__file__).parent / "logs" / "daily_reviews"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"daily-review-{now.strftime('%Y-%m-%d')}.md"

    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"# Daily Paper Trading Review - {now.strftime('%Y-%m-%d')}\n\n")
        f.write(f"**Generated:** {now.strftime('%Y-%m-%d %H:%M:%S')} EAT\n\n")

        if stats:
            f.write("## Performance Summary\n\n")
            f.write(f"- **Total Trades:** {stats['total_trades']}\n")
            f.write(f"- **Win Rate:** {stats['win_rate']:.1f}%\n")
            f.write(f"- **Total P&L:** ${stats['total_pnl_usd']:.2f} USD\n")
            f.write(f"- **Avg P&L:** {stats['avg_pnl_percent']:.2f}%\n\n")
        else:
            f.write("## Performance Summary\n\n")
            f.write("No closed trades yet.\n\n")

        if today_trades:
            f.write(f"## Trades Closed Today ({len(today_trades)})\n\n")
            for trade in today_trades:
                f.write(f"### {trade['symbol']} {trade['side']}\n")
                f.write(f"- **Entry:** ${trade['entry_price_usd']:.2f}\n")
                f.write(f"- **Exit:** ${trade['exit_price_usd']:.2f}\n")
                f.write(f"- **P&L:** {trade['pnl_percent']:.2f}%\n")
                f.write(f"- **Reason:** {trade['exit_reason']}\n\n")

        f.write(f"## Open Positions ({len(open_trades)})\n\n")
        for trade in open_trades:
            f.write(f"- {trade['symbol']} {trade['side']} @ ${trade['entry_price_usd']:.2f}\n")

    print(f"Daily review saved to: {log_file}")

if __name__ == "__main__":
    daily_review()
