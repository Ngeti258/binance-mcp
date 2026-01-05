# Major Cryptocurrencies Market Analysis Command

You are performing a comprehensive hourly market analysis focused on **MAJOR CRYPTOCURRENCIES ONLY** (Top 10-15 by market cap). This excludes small-cap altcoins, meme coins, and emerging tokens.

## Major Coins Definition

**PRIMARY FOCUS (Always Analyze):**
1. **BTC** (Bitcoin) - Market leader
2. **ETH** (Ethereum) - Smart contract leader
3. **BNB** (Binance Coin) - Exchange token
4. **SOL** (Solana) - Fast L1
5. **XRP** (Ripple) - Payment network

**SECONDARY FOCUS (Top 10):**
6. **ADA** (Cardano) - Proof of stake L1
7. **AVAX** (Avalanche) - EVM-compatible L1
8. **DOT** (Polkadot) - Interoperability
9. **MATIC** (Polygon) - Ethereum L2
10. **LINK** (Chainlink) - Oracle network

**TERTIARY FOCUS (If time permits - Top 15):**
11. **UNI** (Uniswap) - DEX leader
12. **ATOM** (Cosmos) - Interchain protocol
13. **LTC** (Litecoin) - Bitcoin fork
14. **TRX** (Tron) - Entertainment L1
15. **DOGE** (Dogecoin) - OG meme coin (included due to market cap)

**EXCLUDED:**
- ❌ Small-cap altcoins (< $1B market cap)
- ❌ New tokens and launches
- ❌ Meme coins (except DOGE due to size)
- ❌ NFT tokens
- ❌ Micro-cap "hidden gems"
- ❌ Pump & dump coins

---

## Analysis Framework

### PHASE 1: Major Coins Data Collection

#### 1A. Currency Conversion (CRITICAL FIRST STEP)

**Get current USD to KES exchange rate using:**
```
mcp__currency-conversion__get_latest_rates
- base: "USD"
- symbols: "KES"
```

**Store rate as:** `USD_TO_KES` (e.g., 129.50)

**Apply dual currency display to ALL monetary values throughout analysis:**
- Format: `$100,000 (KSh 12,950,000)`
- Use consistently in all tables and text

#### 1B. Binance Market Data Collection

**For EACH major coin, collect in parallel:**

Use these Binance MCP tools:
- `mcp__binance-mcp__BinanceTickerPrice` - Current price
- `mcp__binance-mcp__BinanceTicker24hr` - 24h statistics (volume, % change, high, low)
- `mcp__binance-mcp__BinanceDepth` (limit: 100) - Order book analysis
- `mcp__binance-mcp__BinanceKlines` (interval: "1h", limit: 24) - Last 24h of hourly candles
- `mcp__binance-mcp__BinanceAvgPrice` - 5-minute moving average
- `mcp__binance-mcp__BinanceGetTrades` (limit: 100) - Recent trades

**Trading Pairs:**
- BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
- ADAUSDT, AVAXUSDT, DOTUSDT, MATICUSDT, LINKUSDT
- UNIUSDT, ATOMUSDT, LTCUSDT, TRXUSDT, DOGEUSDT

#### 1C. TradingView Technical Indicators

**For EACH major coin, get full indicators:**

Use `mcp__tradingview__get_indicators`:
- symbol: "BTCUSD", "ETHUSD", "BNBUSD", "SOLUSD", "XRPUSD", etc.
- exchange: "BINANCE"
- timeframe: "1h" (for hourly analysis)
- all_indicators: true

**Also get 4h and 1d timeframes for trend context:**
- timeframe: "4h"
- timeframe: "1d"

**Key Indicators to Extract:**
- RSI (Relative Strength Index)
- MACD (momentum)
- Moving Averages (EMA10, EMA20, EMA50, EMA200)
- Bollinger Bands
- Volume indicators
- ADX (trend strength)
- Stochastic
- Recommendation signals (Buy/Sell/Neutral)

#### 1D. News Analysis for Major Coins

**Search crypto news for EACH major coin:**

Use `mcp__crypto-news__get_crypto_news`:
- query: "bitcoin" (max_pages: 2)
- query: "ethereum" (max_pages: 2)
- query: "BNB" (max_pages: 1)
- query: "solana" (max_pages: 2)
- query: "XRP" (max_pages: 2)
- query: "cardano" (max_pages: 1)
- query: "avalanche" (max_pages: 1)
- query: "polkadot" (max_pages: 1)
- query: "polygon" (max_pages: 1)
- query: "chainlink" (max_pages: 1)

**Extract from news:**
- Sentiment (bullish/bearish/neutral)
- Major announcements
- Regulatory news
- Partnership announcements
- Technical upgrades
- Institutional adoption
- ETF news (for BTC/ETH)
- Price predictions from analysts

#### 1E. Social Sentiment Analysis

**Use X/Twitter MCP tools:**

- `mcp__x-mcp-server__get-home-timeline` (maxResults: 10)
- Analyze mentions of major coins
- Identify trending hashtags
- Gauge community sentiment

**Look for:**
- Which major coins are trending
- Bullish vs bearish sentiment
- Influencer opinions on major coins
- FOMO or FUD indicators

#### 1F. Liquidations Data

**Use liquidations MCP:**

`mcp__crypto-liquidations__get_latest_liquidations` (limit: 100)

**Analyze for major coins only:**
- BTC, ETH, BNB, SOL, XRP, ADA, AVAX, DOT, MATIC, LINK, UNI, ATOM, LTC, TRX, DOGE
- Count liquidations per coin
- Long vs short ratio
- Dollar amounts liquidated
- Cascade risk assessment

---

## PHASE 2: Major Coins Analysis

### 2A. Individual Coin Deep Dive

**For EACH major coin (BTC → DOGE), provide:**

#### Price & Market Data
- Current Price (USD & KES)
- 24h Change (% and USD/KES)
- 24h High/Low (USD & KES)
- 24h Volume (USD & KES)
- Market Cap (if available)
- Circulating Supply
- Order Book Analysis:
  - Bid/Ask spread
  - Support levels (USD & KES)
  - Resistance levels (USD & KES)
  - Liquidity depth

#### Technical Analysis (1h, 4h, 1d)
- **RSI:** Value + interpretation (overbought/oversold)
- **MACD:** Signal + momentum direction
- **Moving Averages:** Position relative to EMAs
- **Trend:** Bullish/Bearish/Neutral
- **Support Levels:** Key levels (USD & KES)
- **Resistance Levels:** Key levels (USD & KES)
- **Volume Pattern:** Rising/Falling/Stable
- **Overall Recommendation:** Strong Buy / Buy / Hold / Sell / Strong Sell

#### News & Fundamentals
- News article count (last 24h)
- Sentiment breakdown (% bullish, % bearish, % neutral)
- Top 3 headlines for this coin
- Key catalysts or events
- Regulatory developments

#### Social Sentiment
- Twitter mentions count
- Sentiment (bullish/bearish/neutral)
- Trending status (🔥/📈/📉/—)
- Community FOMO level (1-10)

#### Liquidations Analysis
- Total liquidation events
- Long liquidations (count & USD/KES)
- Short liquidations (count & USD/KES)
- Net bias (longs or shorts getting wrecked)
- Interpretation (squeeze potential, trend continuation, etc.)

### 2B. Comparative Analysis

**Market Leaders Comparison:**

| Coin | Price | 24h % | Volume | Mkt Cap | RSI | MACD | Trend | Sentiment |
|------|-------|-------|--------|---------|-----|------|-------|-----------|
| BTC | $X (KSh X) | +X% | $XB (KSh XB) | $XB | XX | Bullish | 📈 | Bullish |
| ETH | $X (KSh X) | +X% | $XB (KSh XB) | $XB | XX | Bearish | 📉 | Neutral |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Performance Rankings:**
1. Best performer (24h)
2. Worst performer (24h)
3. Highest volume
4. Most bullish technicals
5. Most bearish technicals

**Correlation Analysis:**
- BTC/ETH correlation
- ETH/BNB correlation
- SOL/AVAX correlation
- Which coins moving together
- Which coins diverging

### 2C. Market Dominance & Flow

**Market Cap Distribution:**
- BTC dominance: X%
- ETH dominance: X%
- Top 5 combined: X%
- Top 10 combined: X%

**Capital Flow Patterns:**
- Money flowing INTO: [List coins with rising volume]
- Money flowing OUT OF: [List coins with declining volume]
- BTC → Alts flow? Yes/No (evidence)
- ETH → Alts flow? Yes/No (evidence)
- Smart money vs retail money indicators

---

## PHASE 3: Macro Market Context

### 3A. Overall Market Health

**Market Phase:** Bull Market / Bear Market / Accumulation / Distribution / Correction

**Evidence:**
- BTC trend direction
- ETH trend direction
- Overall volume trends
- Liquidations bias (more longs or shorts)
- News sentiment (% bullish articles)
- Social sentiment (FOMO vs Fear)

### 3B. Risk Assessment

**Market Risks:**
- Regulatory risks (list specific concerns)
- Technical risks (overbought/oversold levels)
- Liquidation cascade risks
- External market risks (stocks, bonds, dollar, etc.)

**Green Flags (Bullish Signals):**
- [List all bullish indicators found]

**Red Flags (Bearish Signals):**
- [List all bearish indicators found]

### 3C. Key Levels to Watch

**Critical Support Levels (USD & KES):**
- BTC: $X (KSh X)
- ETH: $X (KSh X)
- [Other majors...]

**Critical Resistance Levels (USD & KES):**
- BTC: $X (KSh X)
- ETH: $X (KSh X)
- [Other majors...]

**Breakdown Scenarios:**
- If BTC breaks $X → expect [impact]
- If ETH breaks $X → expect [impact]

**Breakout Scenarios:**
- If BTC breaks $X → expect [impact]
- If ETH breaks $X → expect [impact]

---

## PHASE 4: Trading Opportunities

### 4A. Best Long Setups (Next 1-4 Hours)

**For each opportunity, provide:**

**1. [COIN SYMBOL]**
- **Current Price:** $X.XX (KSh X.XX)
- **Entry Zone:** $X.XX - $X.XX (KSh X.XX - KSh X.XX)
- **Target 1:** $X.XX (KSh X.XX) [+X%]
- **Target 2:** $X.XX (KSh X.XX) [+X%]
- **Stop Loss:** $X.XX (KSh X.XX) [-X%]
- **Risk/Reward Ratio:** 1:X
- **Timeframe:** 1-4 hours
- **Rationale:**
  - Technical: [RSI oversold, MACD bullish cross, support bounce, etc.]
  - Fundamental: [News catalyst, positive sentiment, etc.]
  - Risk: [Why this is a good risk/reward]
- **Confidence Level:** High / Medium / Low

**Repeat for top 5 best setups**

### 4B. Best Short Setups (if applicable)

**[Same format as longs]**

### 4C. Hold Recommendations

**Coins to HOLD (not enter):**
- [Coin]: Reason (trending strongly, avoid FOMO entry, wait for pullback)

### 4D. Avoid List

**Coins to AVOID this hour:**
- [Coin]: Reason (overbought, negative news, breakdown, etc.)

---

## Output Format: Comprehensive Major Coins Report

Create a detailed markdown report with the following structure:

```markdown
# 📊 Major Cryptocurrencies Market Analysis
**Generated:** [UTC Timestamp]
**Analysis Period:** Hourly
**Exchange Rate:** 1 USD = X.XX KES

---

## 🎯 Executive Summary

**Market Phase:** [Bull/Bear/Neutral]
**Overall Sentiment:** [Bullish/Bearish/Mixed]
**BTC Dominance:** X.X%
**Total Crypto Market Cap:** $X.XXT (KSh X.XXT)

**Top Performer (24h):** [COIN] +X.X%
**Worst Performer (24h):** [COIN] -X.X%
**Highest Volume:** [COIN] $X.XXB (KSh X.XXB)

**Market Narrative:** [2-3 sentences summarizing the current market situation]

**Key Takeaways:**
- 🔹 [Key point 1]
- 🔹 [Key point 2]
- 🔹 [Key point 3]

---

## 💰 Major Coins Overview

### Bitcoin (BTC)
[Full analysis per template above]

### Ethereum (ETH)
[Full analysis per template above]

### Binance Coin (BNB)
[Full analysis per template above]

### Solana (SOL)
[Full analysis per template above]

### XRP (Ripple)
[Full analysis per template above]

### Cardano (ADA)
[Full analysis per template above]

### Avalanche (AVAX)
[Full analysis per template above]

### Polkadot (DOT)
[Full analysis per template above]

### Polygon (MATIC)
[Full analysis per template above]

### Chainlink (LINK)
[Full analysis per template above]

### [Continue for remaining major coins...]

---

## 📊 Comparative Analysis

### Performance Table
[Table from Phase 2B]

### Performance Rankings
[Rankings from Phase 2B]

### Correlation Matrix
[Correlation analysis from Phase 2B]

---

## 📰 News Analysis Summary

### Top Headlines by Coin
**Bitcoin:**
1. [Headline] - Sentiment: [Bullish/Bearish] - Impact: [High/Medium/Low]
2. [Headline] - Sentiment: [Bullish/Bearish] - Impact: [High/Medium/Low]

**Ethereum:**
[Same format]

**[Continue for all major coins]**

### Overall News Sentiment
- Bullish Articles: XX%
- Bearish Articles: XX%
- Neutral Articles: XX%

### Key Narratives
1. [Narrative 1] - Affecting: [coins]
2. [Narrative 2] - Affecting: [coins]

---

## 🐦 Social Sentiment Summary

**Most Mentioned Coins:**
1. BTC - Sentiment: [Bullish/Bearish] - Intensity: [High/Med/Low]
2. ETH - Sentiment: [Bullish/Bearish] - Intensity: [High/Med/Low]
[...]

**Market FOMO Meter:** X/10
**Market Fear Meter:** X/10

---

## 💥 Liquidations Analysis

### Total Liquidations (Last 100 Events)
- **Total Value:** $X.XXM (KSh X.XXM)
- **Long Liquidations:** XX% ($X.XXM / KSh X.XXM)
- **Short Liquidations:** XX% ($X.XXM / KSh X.XXM)
- **Net Bias:** [Longs/Shorts] getting liquidated more

### Liquidations by Coin
[Table from Phase 1F analysis]

### Interpretation
[Analysis of what liquidations mean for market direction]

---

## 🎯 Trading Opportunities

### 🟢 Best Long Setups (Next 1-4 Hours)
[Detailed setups from Phase 4A]

### 🔴 Best Short Setups
[Detailed setups from Phase 4B if applicable]

### ⏸️ Hold Recommendations
[From Phase 4C]

### ❌ Avoid List
[From Phase 4D]

---

## 🚨 Risk Assessment

### Market Risks
[From Phase 3B]

### Green Flags (Bullish)
[From Phase 3B]

### Red Flags (Bearish)
[From Phase 3B]

### Key Levels to Watch
[From Phase 3C - all levels in USD & KES]

---

## 💡 Market Outlook (Next 4-24 Hours)

**Short-term Prediction (4h):**
[Based on technical analysis, likely movement]

**Medium-term Prediction (24h):**
[Based on news, sentiment, and technical trends]

**Probability Scenarios:**
- 📈 Bullish Scenario (X% probability): [Description]
- ➡️ Sideways Scenario (X% probability): [Description]
- 📉 Bearish Scenario (X% probability): [Description]

---

## ⚠️ Disclaimer

This analysis is for informational purposes only and does not constitute financial advice. Cryptocurrency trading involves substantial risk of loss. Always do your own research (DYOR) and never invest more than you can afford to lose. Past performance does not guarantee future results.

**Data Sources:**
- Binance (Market data)
- TradingView (Technical indicators)
- Crypto News API (News sentiment)
- Twitter/X (Social sentiment)
- Crypto Liquidations (Liquidations data)

**Exchange Rate:** 1 USD = X.XX KES (as of [timestamp])

---

*Analysis generated by Claude Code with MCP integrations*
```

---

## 📝 File Export Instructions

**CRITICAL: Save the complete analysis to a markdown file.**

**File Name Format:** `majors-analysis-{YYYY-MM-DD}-{HH-MM}.md`

**Examples:**
- `majors-analysis-2025-11-08-20-00.md`
- `majors-analysis-2025-11-08-21-00.md`

**Location:** Current working directory

**Steps:**
1. Complete the entire analysis following all phases above
2. Generate the markdown report with full dual currency (USD & KES)
3. Use Write tool to save to file
4. Confirm to user: "✅ Major coins analysis saved to: majors-analysis-{date}-{time}.md"

---

## Execution Checklist

- [ ] **FIRST:** Get USD to KES exchange rate using `mcp__currency-conversion__get_latest_rates`
- [ ] Collected Binance data for ALL 15 major coins
- [ ] Collected TradingView indicators (1h, 4h, 1d) for ALL major coins
- [ ] Searched news for each major coin (BTC, ETH, BNB, SOL, XRP, ADA, AVAX, DOT, MATIC, LINK)
- [ ] Analyzed Twitter/X social sentiment
- [ ] Collected and analyzed liquidations data (filtered for major coins only)
- [ ] **CONVERTED:** All prices, volumes, liquidations to dual USD/KES format
- [ ] Performed individual coin analysis for each major coin
- [ ] Performed comparative analysis (rankings, correlations)
- [ ] Analyzed market dominance and capital flows
- [ ] Assessed overall market health and risks
- [ ] Identified top 5 long opportunities (with entry/target/stop in both currencies)
- [ ] Identified coins to avoid
- [ ] Created comprehensive markdown report with ALL sections
- [ ] **VERIFIED:** All monetary values display both USD and KES correctly
- [ ] **SAVED:** File exported: `majors-analysis-{YYYY-MM-DD}-{HH-MM}.md`
- [ ] **CONFIRMED:** File save location reported to user

---

## Important Notes

**MAJOR COINS ONLY:**
- Focus exclusively on top 15 coins by market cap
- NO small-cap altcoins, meme coins (except DOGE), or new launches
- Deep analysis for each major coin (not surface level)
- Quality over quantity

**Thoroughness:**
- Every major coin gets full analysis (price, technicals, news, social, liquidations)
- Cross-reference multiple data sources
- Provide specific trading setups with risk management
- Dual currency (USD & KES) throughout entire report

**Professional Quality:**
- Comprehensive yet concise
- Data-driven insights
- Clear actionable recommendations
- Proper risk warnings

**Data Quality:**
- Use fresh data (real-time Binance, TradingView)
- Current news (last 24h)
- Recent liquidations (last 100 events)
- Live social sentiment

---

**Now execute this comprehensive MAJOR COINS market analysis!**

---

## 🔄 AUTOMATIC NEXT STEP: Paper Trading Review

**CRITICAL:** After completing the majors analysis and saving the report to file, you MUST automatically trigger the paper trading workflow.

**Do this immediately after confirming the analysis file was saved:**

```markdown
✅ Major coins analysis completed and saved to: majors-analysis-{YYYY-MM-DD}-{HH-MM}.md

---

Now let's review your paper trading portfolio and execute trades based on this analysis.

I'm going to run the /paper-trade command to:
1. Check your open paper trades against current prices
2. Present new trading opportunities from this analysis
3. Let you select which trades to execute
4. Update the paper trading database

Executing: /paper-trade
```

**Then immediately use the SlashCommand tool:**

```typescript
SlashCommand({
    command: "/paper-trade"
})
```

This will:
- ✅ Check all open paper trades for SL/TP hits
- ✅ Present detailed status of open positions
- ✅ Show recently closed trades and performance stats
- ✅ Present new opportunities from this /majors analysis with full context
- ✅ Let user interactively select trades to execute
- ✅ Save executed trades to paper_trades.db
- ✅ Build trading history for 4H strategy development

**DO NOT skip this step** - the paper trading system is how we build data to develop profitable strategies!

---
