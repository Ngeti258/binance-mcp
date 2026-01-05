# Quick Paper Trading Position Monitor with Auto-Close

**Purpose**: Monitor open paper trading positions against live prices and AUTOMATICALLY CLOSE positions when stop loss or targets are hit.

**Frequency**: Every 15-30 minutes during active trading hours
**Runtime**: ~15-30 seconds

---

## IMPORTANT: This command AUTO-CLOSES positions!

When a position hits:
- **Stop Loss** -> Position is CLOSED with loss (status: STOPPED)
- **Target 1** -> Position marked as TP1_HIT (stays open, consider trailing stop)
- **Target 2** -> Position is CLOSED with profit (status: TP2_HIT)

---

## Workflow

### Step 1: Get Open Positions
Query the paper_trades.db for all trades with status IN ('OPEN', 'TP1_HIT')

### Step 2: Fetch Current Prices from Binance
For each unique symbol in open positions, use:
- `mcp__binance-mcp__BinanceTickerPrice` tool

Fetch all prices in PARALLEL for speed.

### Step 3: Check Each Position (AUTO-CLOSE ENABLED)
For each open trade, the database will automatically:
1. Calculate unrealized P&L
2. Check if stop loss is hit -> AUTO-CLOSE if yes
3. Check if target 1 is hit -> Update status to TP1_HIT
4. Check if target 2 is hit -> AUTO-CLOSE if yes
5. Update max favorable/adverse excursion
6. Log the check to trade_checks table

### Step 4: Report Results
Display a summary table showing:
- All positions checked
- Current P&L for each
- Any positions that were CLOSED (stop loss or target)
- Portfolio total unrealized P&L

---

## Output Format

```
=== PAPER TRADING POSITION CHECK ===
Timestamp: 2025-12-09 15:30:00 EAT
Auto-Close: ENABLED

POSITION STATUS (7 trades checked)

Symbol      Side   Entry      Current    P&L%     Status      Action
---------------------------------------------------------------------------
LINKUSDT    LONG   $13.79     $13.50     -2.1%    STOPPED     [CLOSED - Stop Loss Hit]
ETHUSDT     LONG   $3,120     $3,180     +1.9%    TP1_HIT     [Target 1 Reached]
BTCUSDT     LONG   $90,422    $90,600    +0.2%    OPEN        [Monitoring]
XRPUSDT     LONG   $2.062     $2.124     +3.0%    TP2_HIT     [CLOSED - Target 2 Hit]
LTCUSDT     LONG   $83.32     $83.45     +0.2%    OPEN        [Monitoring]
UNIUSDT     SHORT  $5.477     $5.15      +6.0%    TP2_HIT     [CLOSED - Target 2 Hit]
BNBUSDT     SHORT  $887.50    $885.00    +0.3%    OPEN        [Monitoring]

---------------------------------------------------------------------------
CLOSED THIS CHECK: 3 positions
  - LINKUSDT LONG: -2.1% ($-21.00) - Stop Loss
  - XRPUSDT LONG: +3.0% ($+30.00) - Target 2
  - UNIUSDT SHORT: +6.0% ($+60.00) - Target 2

STILL OPEN: 4 positions
Portfolio Unrealized P&L: +$XX.XX (+X.XX%)

Next check recommended: 15-30 minutes
```

---

## Python Code Reference

The auto-close logic is in paper_trading_db.py:

```python
from paper_trading_db import PaperTradingDB

db = PaperTradingDB()

# Get open trades
open_trades = db.get_open_trades()

# For each trade, check against current price
# This AUTOMATICALLY closes if stop/target hit
result = db.update_trade_check(
    trade_id=trade['trade_id'],
    current_price_usd=current_price,
    current_price_kes=current_price * 129.50
)

# Result contains:
# - status: 'OPEN', 'TP1_HIT', 'STOPPED', 'TP2_HIT', 'CLOSED'
# - unrealized_pnl_percent
# - If status changed to STOPPED or TP2_HIT, the trade is now closed
```

---

## Nairobi Timezone Notes

- Best check times: Every 30 minutes from 6AM to 11PM EAT
- Peak volatility: 2PM to 6PM EAT (London/NY overlap)
- FOMC events: Around 10PM EAT (2PM EST)

---

## Alert Priority

1. **CRITICAL**: Position STOPPED (hit stop loss) - Loss realized
2. **SUCCESS**: Position TP2_HIT (hit target 2) - Profit realized
3. **INFO**: Position TP1_HIT (hit target 1) - Consider trailing stop
4. **WARNING**: Large unrealized loss (> -2%) - Monitor closely
5. **NORMAL**: Position within normal range - Continue monitoring
