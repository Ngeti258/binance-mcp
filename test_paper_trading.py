#!/usr/bin/env python3
"""
Test script for paper trading system
Demonstrates creating a sample trade and checking it
"""

from paper_trading_db import PaperTradingDB
from datetime import datetime

def test_paper_trading():
    print("="*60)
    print("PAPER TRADING SYSTEM TEST")
    print("="*60)

    # Initialize database
    db = PaperTradingDB()
    print("\n[1] Database initialized")

    # Create a sample trade
    print("\n[2] Creating sample BTC LONG trade...")

    trade_data = {
        'symbol': 'BTCUSDT',
        'side': 'LONG',
        'strategy': 'RSI_OVERSOLD_MACD_CROSS',
        'timeframe': '1h',
        'entry_price_usd': 96500.00,
        'entry_price_kes': 12498375.00,  # 96500 * 129.50
        'position_size_usd': 1000,
        'stop_loss_usd': 94500.00,
        'stop_loss_kes': 12237750.00,
        'stop_loss_percent': -2.07,
        'target1_usd': 98500.00,
        'target1_kes': 12755750.00,
        'target1_percent': 2.07,
        'target2_usd': 101000.00,
        'target2_kes': 13079500.00,
        'target2_percent': 4.66,
        'risk_reward_ratio': 3.0,
        'rationale': 'Test trade: RSI oversold bounce with bullish MACD cross',
        'market_context': 'Test: BTC dominance rising, market correcting but showing reversal'
    }

    trade_id = db.create_trade(trade_data)
    print(f"   Trade created: {trade_id}")

    # Get open trades
    print("\n[3] Fetching open trades...")
    open_trades = db.get_open_trades()
    print(f"   Open trades: {len(open_trades)}")

    if open_trades:
        trade = open_trades[0]
        print(f"\n   Trade Details:")
        print(f"   - Symbol: {trade['symbol']}")
        print(f"   - Side: {trade['side']}")
        print(f"   - Entry: ${trade['entry_price_usd']:,.2f}")
        print(f"   - Stop Loss: ${trade['stop_loss_usd']:,.2f}")
        print(f"   - Target 1: ${trade['target1_usd']:,.2f}")
        print(f"   - Target 2: ${trade['target2_usd']:,.2f}")
        print(f"   - Risk/Reward: 1:{trade['risk_reward_ratio']}")

    # Simulate price check (price moved to $97,000)
    print("\n[4] Simulating price check at $97,000...")
    current_price_usd = 97000.00
    current_price_kes = 97000.00 * 129.50

    result = db.update_trade_check(trade_id, current_price_usd, current_price_kes)
    print(f"   Current Price: ${result['current_price_usd']:,.2f}")
    print(f"   Status: {result['status']}")
    print(f"   Unrealized P&L: {result['unrealized_pnl_percent']:.2f}%")

    # Get strategy stats
    print("\n[5] Strategy performance...")
    stats = db.get_strategy_stats()
    if stats:
        print(f"   Total trades: {stats['total_trades']}")
        print(f"   Win rate: {stats['win_rate']:.2f}%")
        print(f"   Avg P&L: {stats['avg_pnl_percent']:.2f}%")
    else:
        print("   No closed trades yet (sample trade is still open)")

    # Clean up test trade
    print("\n[6] Closing test trade...")
    db.manually_close_trade(trade_id, 97500.00, 97500.00 * 129.50, "TEST_CLEANUP")
    print("   Test trade closed")

    # Final stats
    print("\n[7] Final stats after closing...")
    stats = db.get_strategy_stats()
    if stats:
        print(f"   Total trades: {stats['total_trades']}")
        print(f"   Wins: {stats['wins']}")
        print(f"   Win rate: {stats['win_rate']:.2f}%")
        print(f"   Total P&L: ${stats['total_pnl_usd']:.2f}")

    print("\n" + "="*60)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nPaper trading system is ready to use!")
    print("Run /majors command in Claude to start trading.")

if __name__ == "__main__":
    test_paper_trading()
