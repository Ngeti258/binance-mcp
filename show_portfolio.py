#!/usr/bin/env python3
import sys
sys.path.append(r'C:\Users\ngeti\Downloads\binance-mcp')

from paper_trading_db import PaperTradingDB

db = PaperTradingDB()

# Get all open trades
open_trades = db.get_open_trades()
print(f'\n=== OPEN POSITIONS ({len(open_trades)} trades) ===\n')

for trade in open_trades:
    side = trade['side']
    symbol = trade['symbol']
    entry = trade['entry_price_usd']
    sl = trade['stop_loss_usd']
    tp1 = trade['target1_usd']
    tp2 = trade['target2_usd']
    rr = trade['risk_reward_ratio']
    sl_pct = trade['stop_loss_percent']
    tp1_pct = trade['target1_percent']
    tp2_pct = trade.get('target2_percent')

    print(f'{symbol} {side}')
    print(f'  Entry: ${entry:.2f}')
    print(f'  Stop Loss: ${sl:.2f} ({sl_pct:.1f}%)')
    print(f'  Target 1: ${tp1:.2f} ({tp1_pct:.1f}%)')
    if tp2:
        print(f'  Target 2: ${tp2:.2f} ({tp2_pct:.1f}%)')
    print(f'  Risk/Reward: 1:{rr:.1f}')
    print(f'  Strategy: {trade["strategy"]}')
    print(f'  Rationale: {trade["rationale"]}')
    print()

# Get strategy stats including the test trade
stats = db.get_strategy_stats()
if stats:
    print('\n=== OVERALL STRATEGY PERFORMANCE ===')
    print(f'Total Closed Trades: {stats["total_trades"]}')
    print(f'Wins: {stats["wins"]} | Losses: {stats["losses"]}')
    print(f'Win Rate: {stats["win_rate"]:.1f}%')
    print(f'Total PnL: ${stats["total_pnl_usd"]:.2f}')
    print(f'Avg PnL: {stats["avg_pnl_percent"]:.2f}%')
