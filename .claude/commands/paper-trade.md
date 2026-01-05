# Paper Trading Review & Execution Command

You are reviewing the paper trading portfolio and executing new trades based on the latest `/majors` analysis.

## CRITICAL SETUP

**Before starting, ensure Python module is importable:**

The paper trading database is managed by `paper_trading_db.py` in the repository root. You'll need to use Python via Bash to interact with it.

---

## WORKFLOW

### PHASE 0: Analyze Lessons Learned (NEW!)

**CRITICAL: Run this FIRST to adjust all recommendations based on historical performance**

```python
import sys
sys.path.append(r'C:\Users\ngeti\Downloads\binance-mcp')
from paper_trading_lessons import TradingLessonsAnalyzer
import json

analyzer = TradingLessonsAnalyzer()

# Get comprehensive lessons
lessons = analyzer.get_lessons_summary()
print(json.dumps(lessons, indent=2, default=str))
```

**Present Lessons Analysis:**

```markdown
## 🎓 Lessons Learned Analysis

### Account Health Status

**Current Risk Level:** {risk_level}
**Win Rate:** {win_rate}% (Target: >50%)
**Total P&L:** {total_pnl_pct}% (Starting: $45,000)

**Adjusted Trading Parameters (Based on Performance):**
- ✅ Maximum Position Size: ${max_position_size} (Normal: $1,000)
- ✅ Required R:R Ratio: {required_rr}:1 (Normal: 2.5:1)
- ✅ Maximum Stop Loss: {max_stop_pct}% (Normal: 2.0%)

**Why These Adjustments?**
{Explain based on current drawdown/win rate - if account is down 30%, explain we're being more conservative}

---

### ❌ STRATEGIES TO AVOID (Poor Historical Performance)

{For each worst strategy:}
**{strategy_name}**
- Win Rate: {win_rate}% ❌
- Record: {wins}W / {losses}L
- Avg Loss: {avg_loss}%
- **Action:** FILTER OUT any opportunities using this strategy

---

### ✅ STRATEGIES TO PRIORITIZE (Strong Historical Performance)

{For each best strategy:}
**{strategy_name}**
- Win Rate: {win_rate}% ✅
- Record: {wins}W / {losses}L
- Avg Win: {avg_win}%
- **Action:** Give PRIORITY to opportunities using this strategy

---

### ⚠️ PROBLEM SYMBOLS (Avoid These Coins)

{For each problem symbol:}
**{symbol}**
- Record: {wins}W / {losses}L ({win_rate}%)
- Total Loss: ${total_pnl}
- **Action:** SKIP all {symbol} trades until pattern breaks

---

### 📊 Recent Performance Trend (Last 7 Days)

- Trades: {recent_trades}
- Win Rate: {recent_win_rate}%
- Trend: {trend} {emoji based on trend}

---
```

### PHASE 1: Review Open Positions

1. **Load Current Prices for All Open Trades**

Use Bash to run Python script that loads open trades and checks them:

```python
import sys
sys.path.append('C:\\Users\\ngeti\\Downloads\\binance-mcp')
from paper_trading_db import PaperTradingDB

db = PaperTradingDB()
open_trades = db.get_open_trades()

# Output for Claude to read
import json
print(json.dumps(open_trades, indent=2, default=str))
```

2. **For Each Open Trade, Get Current Price from Binance**

Use `mcp__binance-mcp__BinanceTickerPrice` for each symbol:
- BTCUSDT
- ETHUSDT
- etc.

3. **Update Trade Status**

For each open trade, call:
```python
result = db.update_trade_check(trade_id, current_price_usd, current_price_kes)
print(json.dumps(result, indent=2, default=str))
```

This automatically:
- Checks if stop loss hit → closes trade
- Checks if target 1 hit → marks as TP1_HIT
- Checks if target 2 hit → closes trade
- Updates max favorable/adverse excursion

4. **Present Open Positions Summary**

Format as a comprehensive table:

```markdown
## 📊 Open Paper Trades Status

| # | Symbol | Side | Entry | Current | Unrealized P&L | Status | Days Open | Actions |
|---|--------|------|-------|---------|----------------|--------|-----------|---------|
| 1 | BTCUSDT | LONG | $95,000 (KSh 12,303,750) | $96,500 (KSh 12,498,375) | +1.58% ($15.80) | OPEN | 2d 4h | 🎯 Near TP1 |
| 2 | ETHUSDT | LONG | $3,500 (KSh 453,250) | $3,450 (KSh 446,775) | -1.43% (-$14.30) | OPEN | 1d 2h | ⚠️ Near SL |

### Detailed Trade Analysis

#### Trade #1: BTC LONG
**Entry Details:**
- Entry Price: $95,000 (KSh 12,303,750)
- Entry Time: 2025-12-04 10:30 UTC (2 days 4 hours ago)
- Position Size: $1,000

**Current Status:**
- Current Price: $96,500 (KSh 12,498,375)
- Unrealized P&L: +1.58% (+$15.80 / +KSh 2,046.15)
- Distance to Stop Loss: -1.58% ($1,500 away)
- Distance to Target 1: +0.42% ($400 away) 🎯 **CLOSE!**
- Distance to Target 2: +3.68% ($3,500 away)

**Risk Levels:**
- Stop Loss: $93,500 (KSh 12,108,250) [-1.58%]
- Target 1: $97,500 (KSh 12,628,125) [+2.63%]
- Target 2: $100,000 (KSh 12,950,000) [+5.26%]

**Performance Metrics:**
- Max Favorable Excursion: +2.1% (best unrealized profit)
- Max Adverse Excursion: -0.8% (worst unrealized loss)

**Original Rationale:**
RSI oversold bounce at 42 + bullish MACD cross on 1h timeframe. Price bouncing off 200 EMA support. Positive ETF inflow news. Risk/Reward: 1:3.0

**Action Recommendation:**
✅ **Consider partial close at TP1** - Target 1 is only $400 away. Could lock in +2.63% profit on 50% of position and let rest run to TP2.

---

#### Trade #2: ETH LONG
**Entry Details:**
- Entry Price: $3,500 (KSh 453,250)
- Entry Time: 2025-12-05 08:15 UTC (1 day 2 hours ago)
- Position Size: $1,000

**Current Status:**
- Current Price: $3,450 (KSh 446,775)
- Unrealized P&L: -1.43% (-$14.30 / -KSh 1,851.85)
- Distance to Stop Loss: -1.43% ($50 away) ⚠️ **DANGER ZONE!**
- Distance to Target 1: +1.43% ($50 away)

**Risk Levels:**
- Stop Loss: $3,400 (KSh 440,300) [-2.86%]
- Target 1: $3,600 (KSh 466,200) [+2.86%]

**Performance Metrics:**
- Max Favorable Excursion: +0.5%
- Max Adverse Excursion: -1.8%

**Original Rationale:**
Support bounce at key $3,500 level. Looking for bounce to $3,600 resistance.

**Action Recommendation:**
⚠️ **Monitor closely** - Price hovering near stop loss. Consider:
1. Manual close to cut losses early (-1.43% vs -2.86%)
2. Let it hit SL if you trust the setup
3. Widen SL if you believe in the trade (risky!)
```

---

### PHASE 2: Show Recently Closed Trades

Get closed trade history:
```python
closed_trades = db.get_trade_history(limit=10)
print(json.dumps(closed_trades, indent=2, default=str))
```

Present as:

```markdown
## 💰 Recently Closed Trades (Last 10)

| # | Symbol | Side | Entry | Exit | P&L % | P&L $ | Result | Exit Reason | Trade Duration |
|---|--------|------|-------|------|-------|-------|--------|-------------|----------------|
| 1 | SOLUSDT | LONG | $120.00 | $126.00 | +5.00% | +$50.00 | ✅ WIN | TARGET1 | 4h 30m |
| 2 | XRPUSDT | SHORT | $0.65 | $0.67 | -3.08% | -$30.80 | ❌ LOSS | STOP_LOSS | 2h 15m |
| 3 | ADAUSDT | LONG | $0.50 | $0.52 | +4.00% | +$40.00 | ✅ WIN | TARGET1 | 6h 45m |
| 4 | BNBUSDT | LONG | $620.00 | $610.00 | -1.61% | -$16.10 | ❌ LOSS | STOP_LOSS | 1h 20m |
| 5 | LINKUSDT | LONG | $18.00 | $19.50 | +8.33% | +$83.30 | ✅ WIN | TARGET2 | 12h 10m |

**Quick Stats from Last 10:**
- Wins: 6 (60%)
- Losses: 4 (40%)
- Total P&L: +$126.40 (+12.64%)
- Best Trade: LINK LONG +8.33%
- Worst Trade: XRP SHORT -3.08%
```

---

### PHASE 3: Show Overall Strategy Performance

Get strategy stats:
```python
stats = db.get_strategy_stats()
if stats:
    print(json.dumps(stats, indent=2, default=str))
else:
    print("No closed trades yet")
```

Present as:

```markdown
## 📈 Paper Trading Performance Summary

**Overall Statistics:**
- 📊 Total Trades: 45
- ✅ Winning Trades: 26 (57.78%)
- ❌ Losing Trades: 19 (42.22%)
- 💰 Total P&L: +$567.50 (+12.61% cumulative)
- 📈 Average P&L per Trade: +1.26%

**Win/Loss Analysis:**
- Average Win: +3.21%
- Average Loss: -1.85%
- Best Trade: SOL LONG +12.50%
- Worst Trade: MATIC LONG -5.20%

**Current Status:**
- Open Trades: 2
- Account Equity: $45,567.50 (starting: $45,000)
- Unrealized P&L: +$1.50 (+0.003%)

**Performance Rating:**
- Win Rate: 57.78% ⭐⭐⭐⭐ (Excellent - above 55%)
- Avg R:R Realized: 1.73:1 ⭐⭐⭐ (Good - above 1.5)
- Total Return: +1.26% ⭐⭐⭐ (Good progress)

**What's Working:**
- ✅ RSI oversold bounces: 65% win rate
- ✅ MACD crosses with volume: 70% win rate
- ✅ Support bounces: 58% win rate

**What's Not Working:**
- ❌ Breakout trades: 40% win rate
- ❌ Counter-trend trades: 35% win rate
```

---

### PHASE 4: Present New Trade Opportunities (WITH LESSONS-BASED FILTERING)

**CRITICAL: Filter opportunities through lessons learned before presenting**

Based on the `/majors` analysis that was just run, read the latest analysis file and FILTER each opportunity:

```python
import glob
import os
import sys
sys.path.append(r'C:\Users\ngeti\Downloads\binance-mcp')
from paper_trading_lessons import TradingLessonsAnalyzer

analyzer = TradingLessonsAnalyzer()

# Find most recent majors analysis
files = glob.glob('majors-analysis-*.md')
if files:
    latest = max(files, key=os.path.getctime)
    with open(latest, 'r', encoding='utf-8') as f:
        analysis_content = f.read()

    # Extract trading opportunities section
    # Look for "## 🎯 Trading Opportunities" section

# For EACH opportunity, check if it should be filtered
# Example opportunity structure:
opportunities = [
    {
        'symbol': 'BTCUSDT',
        'strategy': 'RSI_OVERSOLD_BOUNCE',
        'stop_loss_percent': 2.5,
        'risk_reward_ratio': 2.0
    }
]

filtered_opportunities = []
excluded_opportunities = []

for opp in opportunities:
    should_filter, reason = analyzer.should_filter_opportunity(opp)

    if should_filter:
        excluded_opportunities.append({
            'opportunity': opp,
            'exclusion_reason': reason
        })
    else:
        # Add historical context
        context = analyzer.get_enhanced_opportunity_context(opp)
        opp['historical_context'] = context
        filtered_opportunities.append(opp)
```

**FIRST: Show EXCLUDED opportunities (Learning in Action!)**

```markdown
## 🚫 Opportunities EXCLUDED Based on Lessons Learned

{For each excluded opportunity:}

### ❌ {symbol} {side} - **FILTERED OUT**

**Why This Trade Was Excluded:**
{exclusion_reason}

**Setup That Was Proposed:**
- Entry: ${entry_price}
- Stop Loss: ${stop_loss} ({stop_loss_percent}%)
- Target: ${target}
- R:R: {rr_ratio}

**Lesson Applied:**
This trade was automatically filtered because our historical data shows this pattern/symbol/strategy has poor performance. We're protecting capital by avoiding repeating past mistakes.

---
```

**THEN: Present APPROVED opportunities with enhanced historical context:**

```markdown
## 🎯 New Trade Opportunities from Latest Analysis

### Trade Opportunity #1: BTC LONG 📈

**Setup Details:**
- Symbol: BTCUSDT
- Side: LONG
- Current Price: $96,500 (KSh 12,498,375)
- Entry Zone: $96,000 - $96,800 (KSh 12,432,000 - 12,535,600)

**Risk Management:**
- 🛑 Stop Loss: $94,500 (KSh 12,237,750) [-1.56%]
- 🎯 Target 1: $98,500 (KSh 12,755,750) [+2.07%]
- 🎯 Target 2: $101,000 (KSh 13,079,500) [+4.66%]
- ⚖️ Risk/Reward: 1:3.0 (Excellent!)

**Technical Analysis (1h):**
- RSI: 42 → Oversold region, room to bounce
- MACD: Bullish cross just formed
- Price: Bouncing off 200 EMA support at $95,800
- Volume: Increasing +25% on recent green candles
- Trend: Downtrend but showing reversal signs

**Multi-Timeframe Confirmation:**
- 4h: RSI 38 (oversold), MACD turning bullish
- 1d: Price at key support zone, not oversold yet

**Fundamental Context:**
- 📰 News Sentiment: Bullish (68% positive)
  - Top headline: "BlackRock BTC ETF sees $150M inflow"
  - MicroStrategy announces additional $500M BTC purchase
- 🐦 Social Sentiment: Mixed-to-bullish
- 💥 Liquidations: $12.5M shorts liquidated in last 4h (squeeze potential)

**Market Context:**
- BTC Dominance: 52.3% (+0.5% today) → Money flowing to BTC
- Overall Market: Corrective phase but showing reversal
- Correlation: ETH following BTC closely (0.85 correlation)

**Historical Performance Analysis (AUTOMATED FROM DATABASE):**

{If strategy has history:}
📊 **Strategy Track Record: "{strategy_name}"**
- Win Rate: {win_rate}% ({wins}W / {losses}L)
- Average Win: +{avg_win}%
- Average Loss: {avg_loss}%
- Recommendation: {recommendation}
- **Confidence Adjustment:** {+1 if good, -2 if bad}

{If symbol has history:}
📈 **{Symbol} Performance History:**
- Win Rate: {win_rate}% ({wins}W / {losses}L)
- Total P&L: ${total_pnl}
- Recommendation: {recommendation}
- **Confidence Adjustment:** {+1 if good, -3 if terrible}

{If no history:}
⚠️ **No Historical Data:** This is a new strategy/symbol combination - no past performance data available.

**Overall Confidence Adjustment:** {total adjustment from strategy + symbol}
- Base Confidence: {original}/10
- Adjusted Confidence: {original + adjustments}/10

**Why This Trade Makes Sense:**
BTC is showing strong signs of bottoming on the 1h timeframe after a sharp -8% correction from $104k. The combination of oversold RSI (42), fresh bullish MACD cross, and price bouncing precisely off the 200 EMA creates a high-probability reversal setup.

Fundamentals support the bounce: positive ETF flows, institutional buying from MicroStrategy, and shorts getting squeezed ($12.5M liquidated). The 4h timeframe confirms oversold conditions.

Risk is well-defined at $94,500 (below 200 EMA), while upside potential is $98,500 (previous resistance) and $101,000 (psychological level). R:R of 1:3 is excellent.

**Portfolio Impact if Executed:**
- Current Exposure: 2 open trades, $2,000 total
- New Exposure: 3 trades, $3,000 total (6.67% of $45k account)
- Correlation: Low (no other BTC positions)
- Risk: -1.56% max loss = -$15.60

**ADJUSTED POSITION SIZING (Based on Account Health):**
- Normal Position Size: $1,000
- Adjusted Size: ${adjusted_size}
- Reason: {If account in drawdown, explain we're reducing size; if healthy, keep at $1000}
- **This trade will use ${adjusted_size}**

**Confidence Level:** ⭐⭐⭐⭐⭐ HIGH (9/10)

**My Recommendation:**
✅ **EXECUTE** - This is a textbook high-probability setup with excellent R:R, multi-timeframe confirmation, and strong fundamentals. Historical data shows 65% win rate for this pattern.

---

### Trade Opportunity #2: ETH LONG 📈

[Same detailed format for each opportunity...]

---

### Trade Opportunity #3: SOL LONG 📈

[Same detailed format...]

---

## ⚠️ Additional Context: Why Some Opportunities Were Skipped

**Opportunities from analysis that didn't make the cut:**

{List any other opportunities from /majors that weren't presented, with data-driven reasoning:}

### ❌ {Symbol} {Side}
- Setup: {description}
- **Data-Driven Exclusion Reason:**
  - Historical Performance: {If available: X% win rate (XW/XL), -$XX total loss}
  - Strategy Issue: {If applicable: This strategy has Y% win rate across Z trades}
  - Risk Mismatch: {If applicable: Stop loss X% exceeds our max Y% for current account health}
  - R:R Issue: {If applicable: R:R of X:1 below required Y:1 for recovery mode}
- **Bottom Line:** {Specific reason based on actual data, not hunches}

---

**NOTE:** All exclusions above are based on YOUR actual historical trading data. These aren't arbitrary decisions—they're lessons learned from your {total_trades} trades and {win_rate}% win rate.
```

---

### PHASE 5: Interactive Trade Selection

Use `AskUserQuestion` to let user select trades:

```markdown
Now I'll present you with all available actions. You can select multiple:
```

**Questions to ask:**

1. **New Trades to Execute:**
```json
{
  "question": "Which new paper trades would you like to execute?",
  "header": "New Trades",
  "multiSelect": true,
  "options": [
    {
      "label": "BTC LONG @ $96,500",
      "description": "R:R 1:3.0, Win Rate: 65%, Confidence: HIGH (9/10)"
    },
    {
      "label": "ETH LONG @ $3,550",
      "description": "R:R 1:2.8, Win Rate: 58%, Confidence: MEDIUM (7/10)"
    },
    {
      "label": "SOL LONG @ $145",
      "description": "R:R 1:4.2, Win Rate: 70%, Confidence: HIGH (8/10)"
    }
  ]
}
```

2. **Manage Open Positions:**
```json
{
  "question": "Any actions on existing open trades?",
  "header": "Open Trades",
  "multiSelect": true,
  "options": [
    {
      "label": "Close BTC LONG (take profit)",
      "description": "Current: +1.58% profit, near TP1. Lock in gains?"
    },
    {
      "label": "Close ETH LONG (cut loss)",
      "description": "Current: -1.43% loss, near SL. Cut early to save 1.43%?"
    },
    {
      "label": "No changes - let them run",
      "description": "Keep all positions as-is and let SL/TP manage"
    }
  ]
}
```

---

### PHASE 6: Execute Selected Trades

For **each new trade** the user selected:

1. **Get exact current price:**
```python
# Use MCP tool
price_data = mcp__binance-mcp__BinanceTickerPrice(symbol="BTCUSDT")
current_price = float(price_data['price'])

# Get USD to KES rate
rate_data = mcp__currency-conversion__get_latest_rates(base="USD", symbols="KES")
usd_to_kes = rate_data['rates']['KES']
```

2. **Create trade in database with ADJUSTED position size:**
```python
from paper_trading_db import PaperTradingDB
from paper_trading_lessons import TradingLessonsAnalyzer

db = PaperTradingDB()
analyzer = TradingLessonsAnalyzer()

# Get adjusted position size based on account health
health = analyzer.get_account_health_metrics()
adjusted_position_size = health['max_position_size']

trade_id = db.create_trade({
    'symbol': 'BTCUSDT',
    'side': 'LONG',
    'strategy': 'RSI_OVERSOLD_MACD_CROSS_EMA200_BOUNCE',
    'timeframe': '1h',
    'entry_price_usd': 96500,
    'entry_price_kes': 96500 * usd_to_kes,
    'position_size_usd': adjusted_position_size,  # ADJUSTED based on account health!
    'stop_loss_usd': 94500,
    'stop_loss_kes': 94500 * usd_to_kes,
    'stop_loss_percent': -2.07,
    'target1_usd': 98500,
    'target1_kes': 98500 * usd_to_kes,
    'target1_percent': 2.07,
    'target2_usd': 101000,
    'target2_kes': 101000 * usd_to_kes,
    'target2_percent': 4.66,
    'risk_reward_ratio': 3.0,
    'rationale': 'RSI oversold bounce (42) with bullish MACD cross on 1h timeframe. Price bouncing precisely off 200 EMA support. Positive ETF inflows and short squeeze building. Historical 65% win rate for this pattern.',
    'market_context': 'BTC dominance rising (52.3%), overall market corrective but reversing. ETF inflows positive. $12.5M shorts liquidated. 4h timeframe confirms oversold.',
    'analysis_snapshot': {
        'rsi_1h': 42,
        'macd_1h': 'bullish_cross',
        'rsi_4h': 38,
        'price_vs_200ema': 'bounce',
        'volume_change': '+25%'
    }
})

print(f"Trade executed: {trade_id}")
```

3. **Confirm to user with risk adjustment explanation:**
```markdown
✅ **Paper Trade Executed: BTC LONG**

**Trade ID:** `BTCUSDT_LONG_20251206_143052`

**Entry Details:**
- Symbol: BTCUSDT
- Side: LONG
- Entry Price: $96,500.00 (KSh 12,498,375.00)
- Entry Time: 2025-12-06 14:30:52 UTC
- Position Size: ${adjusted_position_size} {If different from $1000: ⚠️ REDUCED}

{If position size was adjusted:}
**Risk Management Note:**
Position size adjusted from normal $1,000 to ${adjusted_position_size} because:
- Account Health: {risk_level}
- Current Win Rate: {win_rate}%
- Account Drawdown: {total_pnl_pct}%
- **Strategy:** Being more conservative to protect capital during recovery phase

**Risk Management:**
- Stop Loss: $94,500 (KSh 12,237,750) [-2.07%]
- Target 1: $98,500 (KSh 12,755,750) [+2.07%]
- Target 2: $101,000 (KSh 13,079,500) [+4.66%]
- Risk/Reward: 1:3.0

**Strategy:** RSI_OVERSOLD_MACD_CROSS_EMA200_BOUNCE

**Saved to Database:** ✅ `paper_trades.db`

---
```

For **position management** actions:

```python
# If user chose to close a trade early
db.manually_close_trade(
    trade_id='BTCUSDT_LONG_20251204_103000',
    exit_price_usd=96500,
    exit_price_kes=96500 * usd_to_kes,
    reason='MANUAL_CLOSE_PROFIT_TAKING'
)
```

Confirm:
```markdown
✅ **Position Closed: BTC LONG**

**Trade ID:** `BTCUSDT_LONG_20251204_103000`

**Performance:**
- Entry: $95,000 (2 days ago)
- Exit: $96,500 (now)
- P&L: +1.58% (+$15.80)
- Exit Reason: Manual profit taking
- Duration: 2d 4h

**Trade saved to history**
```

---

### PHASE 7: Session Summary

```markdown
## 📋 Paper Trading Session Complete

**Timestamp:** 2025-12-06 14:35 UTC

---

### Actions Taken This Session

**Trades Reviewed:**
- ✅ Checked 2 open positions
- ✅ Updated all trade statuses vs current prices
- ✅ Logged price checks to database

**Positions Closed:**
- ✅ BTC LONG: +1.58% (manual profit taking)

**New Trades Executed:**
- ✅ BTC LONG @ $96,500 (Trade ID: BTCUSDT_LONG_20251206_143052)
- ✅ SOL LONG @ $145.50 (Trade ID: SOLUSDT_LONG_20251206_143055)

**Trades Declined:**
- ❌ ETH LONG (user chose not to enter)
- ❌ XRP SHORT (not recommended - counter-trend)

---

### Updated Portfolio Status

**Open Positions:** 3
1. BTC LONG - Entry: $96,500, Status: OPEN
2. SOL LONG - Entry: $145.50, Status: OPEN
3. ETH LONG - Entry: $3,500, Status: OPEN (⚠️ near SL)

**Portfolio Exposure:**
- Total Capital Allocated: $3,000 (6.67% of account)
- Risk if all SL hit: -$56.40 (-1.25% of account)
- Potential reward if all TP1 hit: +$67.20 (+1.49% of account)

---

### Performance Update

**Closed Trades:** 46 total
- Win Rate: 58.70% (27W / 19L)
- Total P&L: +$583.30 (+12.96%)
- Average P&L: +1.27%

**Compared to Last Session:**
- Win rate: 58.70% (was 57.78%) ⬆️ +0.92%
- Total P&L: +$583.30 (was $567.50) ⬆️ +$15.80

---

### Database Status

**Files Updated:**
- ✅ `paper_trades.db` - All trades logged
- ✅ `trade_checks` table - Price updates logged
- ✅ Latest analysis: `majors-analysis-2025-12-06-14-09.md`

**Records:**
- Total trades in DB: 49
- Trade checks logged: 157
- Closed trades: 46
- Open trades: 3

---

### Next Steps

**1. Monitor Positions:**
Next `/majors` run will automatically check all open trades

**2. Key Levels to Watch:**
- BTC: Watch for TP1 at $98,500 (1.58% away)
- ETH: DANGER - Only $50 from SL ($3,400)
- SOL: Fresh entry, monitor for first hour

**3. Recommended Actions Before Next Session:**
- If ETH drops to $3,425, consider manual close to save 0.71%
- If BTC hits $98,000, consider moving SL to breakeven ($96,500)

---

### Learning Insights

**What Worked Today:**
- ✅ Manual profit taking on BTC (+1.58%) avoided giving back gains
- ✅ Declining ETH setup based on poor entry timing saved potential loss

**What to Watch:**
- ⚠️ ETH trade struggling - may need to refine support bounce entries
- ⚠️ Portfolio now has 3 correlated positions (all LONG) - consider diversification

---

### 🎓 Lessons Learned Impact This Session

**Automated Filters Applied:**
- 🚫 Filtered out {X} opportunities based on historical data
- ✅ Approved {Y} opportunities that passed lessons screening
- 📊 Applied {risk_level} risk parameters (account at {total_pnl_pct}%)

**Capital Protected by Filters:**
{If opportunities were filtered out:}
- Avoided repeating {strategy_name} which has {win_rate}% win rate
- Skipped {symbol} which has cost us ${total_loss} historically
- **Estimated loss avoided:** ~${estimated_loss} (based on historical avg loss)

**Risk Adjustments Made:**
- Position sizes: {If adjusted: Reduced to $X from $1,000} {If normal: Standard $1,000}
- Required R:R: {required_rr}:1 (Normal: 2.5:1)
- Max Stop: {max_stop_pct}% (Normal: 2.0%)

**Database Learning Stats:**
- Total strategies analyzed: {total_strategies}
- Total symbols analyzed: {total_symbols}
- Worst performing strategy: {name} at {win_rate}%
- Best performing strategy: {name} at {win_rate}%

**Progress Tracking:**
- Win rate trend: {If improving: 📈 Improving} {If declining: 📉 Needs attention}
- Recent 7-day performance: {recent_win_rate}% ({trend})
- Lessons applied automatically: Preventing repeat mistakes ✅

---

**Next Analysis:** Run `/majors` in 1 hour to check trade progress

**Paper Trading Database:** `C:\Users\ngeti\Downloads\binance-mcp\paper_trades.db`
**Lessons Analyzer:** `C:\Users\ngeti\Downloads\binance-mcp\paper_trading_lessons.py`
```

---

## EXECUTION CHECKLIST

Before completing, verify:

**NEW - Lessons Learned Phase:**
- [ ] ✨ Loaded paper_trading_lessons.py analyzer
- [ ] ✨ Analyzed account health and got risk adjustments
- [ ] ✨ Identified worst performing strategies to avoid
- [ ] ✨ Identified best performing strategies to prioritize
- [ ] ✨ Identified problem symbols to skip
- [ ] ✨ Presented lessons learned summary to user
- [ ] ✨ Filtered ALL opportunities through lessons analyzer
- [ ] ✨ Showed excluded opportunities with data-driven reasons
- [ ] ✨ Added historical context to approved opportunities
- [ ] ✨ Applied adjusted position sizes based on account health

**Standard Phases:**
- [ ] Loaded paper_trades.db successfully
- [ ] Checked ALL open trades with current prices
- [ ] Updated trade statuses (SL/TP checks)
- [ ] Presented open positions with detailed analysis
- [ ] Showed recently closed trades (last 10)
- [ ] Calculated and displayed strategy performance stats
- [ ] Read latest `/majors` analysis file
- [ ] Used lessons analyzer to filter opportunities
- [ ] Presented only approved opportunities with historical data
- [ ] Calculated portfolio impact for new trades
- [ ] Used AskUserQuestion for trade selection
- [ ] Executed selected trades with adjusted position sizes
- [ ] Confirmed each trade with risk adjustment notes
- [ ] Closed positions if user requested
- [ ] Generated comprehensive session summary
- [ ] Included lessons learned impact section
- [ ] Provided actionable next steps

---

## IMPORTANT NOTES

**Data Integrity:**
- Always use `json.dumps(default=str)` when printing datetime objects
- Verify trade_id is unique before creating
- Double-check USD to KES conversion is current

**Risk Management:**
- Maximum 5 concurrent open trades
- Maximum 10% total portfolio exposure
- Never exceed 2% risk per trade

**Learning:**
- Always reference historical performance for similar setups
- Track which strategies are working (win rate > 55%)
- Identify patterns that aren't working (win rate < 45%)

**User Experience:**
- Be honest about confidence levels
- Explain reasoning clearly
- Don't oversell trades
- Highlight risks, not just rewards

---

**Now execute the paper trading review and execution workflow!**
