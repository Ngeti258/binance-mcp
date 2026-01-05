# Single Altcoin Deep Analysis Command

**Usage:** `/analyze <SYMBOL>`

**Examples:**
- `/analyze XRP`
- `/analyze DOGE`
- `/analyze PEPE`

---

You are performing a comprehensive deep-dive analysis on a SINGLE altcoin specified by the user. This is an on-demand, focused analysis that provides everything needed to make an informed trading decision on this specific coin.

## Input Processing

**User will provide:** Symbol name (e.g., "XRP", "DOGE", "PEPE")

**Your first step:**
1. Extract the symbol from user input
2. Normalize to uppercase (e.g., "xrp" → "XRP")
3. Construct trading pairs:
   - USDT pair: `{SYMBOL}USDT` (e.g., XRPUSDT)
   - USD pair for TradingView: `{SYMBOL}USD` (e.g., XRPUSD)
4. Confirm with user: "Analyzing [SYMBOL]. Collecting data..."

---

## Analysis Framework

### PHASE 1: Market Data Collection (Binance)

Collect comprehensive Binance data for the altcoin:

**Use these tools in parallel:**
1. `mcp__binance-mcp__BinanceTickerPrice` - symbol: {SYMBOL}USDT
2. `mcp__binance-mcp__BinanceTicker24hr` - symbol: {SYMBOL}USDT
3. `mcp__binance-mcp__BinanceDepth` - symbol: {SYMBOL}USDT, limit: 100
4. `mcp__binance-mcp__BinanceKlines` - symbol: {SYMBOL}USDT, interval: 1h, limit: 24
5. `mcp__binance-mcp__BinanceKlines` - symbol: {SYMBOL}USDT, interval: 4h, limit: 24
6. `mcp__binance-mcp__BinanceKlines` - symbol: {SYMBOL}USDT, interval: 1d, limit: 30
7. `mcp__binance-mcp__BinanceAvgPrice` - symbol: {SYMBOL}USDT
8. `mcp__binance-mcp__BinanceAggTrades` - symbol: {SYMBOL}USDT, limit: 100

**Also collect BTC/ETH for context:**
- BTC: Price, 24h change only
- ETH: Price, 24h change only

**Extract from data:**
- Current price and 5-min average
- 24h price change %, volume, high, low
- Order book support/resistance levels
- Hourly, 4-hour, daily candle patterns
- Recent large trades (from agg trades)
- Bid/ask spread and liquidity

---

### PHASE 2: Technical Analysis (TradingView)

Get complete technical indicators for the altcoin:

**Use `mcp__tradingview__get_indicators`:**
- symbol: {SYMBOL}USD
- exchange: BINANCE
- timeframe: 1h
- all_indicators: true

**Repeat for multiple timeframes:**
- 1h (short-term)
- 4h (medium-term)
- 1d (long-term trend)

**Analyze all indicators:**
- RSI (14) - Overbought/oversold levels
- MACD - Momentum and crossovers
- Stochastic - Additional oversold/overbought confirmation
- Moving Averages - EMA/SMA 10, 20, 50, 100, 200
- Bollinger Bands - Volatility and position
- ADX - Trend strength
- CCI - Commodity Channel Index
- Volume indicators
- Pivot points (support/resistance)
- Overall recommendation (Buy/Sell/Neutral)

**Compare across timeframes:**
- 1h trend vs 4h trend vs daily trend
- Confluence of signals
- Divergences between timeframes

---

### PHASE 3: News & Sentiment Analysis

**3A. Crypto News Deep Dive**

Search extensively for coin-specific news:

**Use `mcp__crypto-news__get_crypto_news` with multiple queries:**
1. "{SYMBOL}" - max_pages: 5
2. "{FULL_NAME}" (e.g., "Ripple" for XRP) - max_pages: 3
3. "{SYMBOL} price" - max_pages: 2
4. "{SYMBOL} prediction" - max_pages: 2
5. "{SYMBOL} ETF" or "{SYMBOL} SEC" - max_pages: 2 (if relevant)
6. "{SYMBOL} partnership" - max_pages: 1
7. "{SYMBOL} upgrade" - max_pages: 1

**Also search related narratives:**
- If meme coin: "meme coin", "memecoin rally"
- If Layer 2: "layer 2", "ethereum scaling"
- If DeFi: "defi", "TVL"
- If AI: "AI crypto", "artificial intelligence"
- If gaming: "gaming token", "metaverse"

**Analyze all news articles:**
- Count total articles (last 24h)
- Sentiment breakdown (% bullish, bearish, neutral)
- Key themes and narratives
- Catalysts mentioned (partnerships, upgrades, listings, etc.)
- Price predictions from analysts
- Regulatory developments
- Competitive position vs similar coins

**3B. Twitter Social Sentiment**

**Use X MCP tools:**
- `mcp__x-mcp-server__get-home-timeline` (maxResults: 10) - Look for mentions
- Search for ${SYMBOL} hashtag mentions
- Identify influencer opinions

**Analyze:**
- Mention frequency and volume
- Sentiment (bullish/bearish/neutral)
- Trending hashtags (#{SYMBOL}, #{SYMBOL}Army, etc.)
- Community excitement level (FOMO vs Fear)
- Influencer predictions and price targets
- Comparison mentions ("next Bitcoin", "better than X")
- Shilling intensity

---

### PHASE 4: Liquidations Analysis

**Use `mcp__crypto-liquidations__get_latest_liquidations` (limit: 100)**

**Filter for {SYMBOL}:**
- Count liquidations for {SYMBOL}USDT
- Calculate long vs short liquidation ratio
- Sum total $ liquidated
- Identify largest single liquidation
- Analyze timing patterns

**Interpret:**
- If shorts liquidated (>60%) = bullish squeeze
- If longs liquidated (>60%) = bearish pressure
- Large liquidations = volatility and interest
- No liquidations = low interest/volume
- Recent spike in liquidations = potential reversal

**Compare to other altcoins:**
- Is {SYMBOL} in top 10 liquidated coins?
- Relative liquidation intensity

---

### PHASE 5: Correlation & Context Analysis

**5A. Compare to BTC/ETH**
- Is {SYMBOL} outperforming or underperforming BTC?
- Correlation coefficient (moving with or against BTC)
- Beta vs BTC (volatility comparison)

**5B. Compare to Sector Peers**

Identify sector and compare:
- If XRP → Compare to other payment coins (XLM, ALGO)
- If meme coin → Compare to DOGE, SHIB, PEPE
- If Layer 2 → Compare to ARB, OP, MATIC
- If DeFi → Compare to UNI, AAVE, MKR
- If AI → Compare to FET, AGIX, RNDR

**Collect 24h data for 3-5 peers:**
- Price change %
- Volume comparison
- Which is leading the sector?

**5C. Historical Performance**
From 30-day klines data:
- 7-day performance
- 30-day performance
- ATH distance (how far from all-time high?)
- Major support/resistance from history

---

### PHASE 6: On-Chain & Exchange Metrics (if available)

**Try to find:**
- Binance trading volume rank
- Number of trading pairs
- Recent listings or delistings
- Funding rate (for futures)
- Open interest trends

---

## Currency Conversion (Kenyan Shillings)

**CRITICAL STEP - Must do FIRST before analysis:**

Use Currency Conversion MCP to get current USD to KES exchange rate:

**Use `mcp__currency-conversion__get_latest_rates`:**
- base: "USD"
- symbols: "KES"

This returns the current USD/KES exchange rate (e.g., 1 USD = 129.50 KES)

**Store this rate as:** `USD_TO_KES`

**For ALL price/volume/liquidation values in the report:**
1. Keep USD value
2. Calculate KES value: USD_value × USD_TO_KES
3. Display BOTH in reports:
   - Format: `$1,234 (KSh 159,843)`
   - Or in tables: `$1,234 | KSh 159,843`

**Currency Display Format:**
- USD: Use $ symbol, comma separators (e.g., $1,234.56)
- KES: Use KSh or Ksh, comma separators (e.g., KSh 159,843.20)

**Apply conversion to:**
- {SYMBOL} price (current, high, low, averages)
- All volumes (24h volume, etc.)
- All liquidation amounts
- Support/resistance levels
- Entry/target/stop prices
- All dollar values mentioned

**Example Conversions:**
- XRP $2.30 → $2.30 (KSh 297.85)
- Volume $500M → $500M (KSh 64.75B)
- Entry $2.25 → $2.25 (KSh 291.38)
- Stop $2.15 → $2.15 (KSh 278.43)

---

## Output Format: Comprehensive Single-Coin Report

Create detailed markdown report:

---

# 🔍 Deep Analysis: {SYMBOL}

**Generated:** [Timestamp]
**Analysis Type:** Single Altcoin Focus
**Timeframe:** Multi-timeframe (1h, 4h, 1d)
**Exchange Rate:** 1 USD = [X.XX] KES

---

## 📊 Executive Summary

**Coin:** {FULL_NAME} ({SYMBOL})
**Current Price:** $X.XX (KSh X,XXX.XX)
**24h Change:** +/- X.XX%
**Market Sentiment:** Bullish/Bearish/Neutral
**Technical Signal:** Strong Buy / Buy / Neutral / Sell / Strong Sell
**News Sentiment:** X/10 (Bullish/Bearish)
**Social Buzz:** High/Medium/Low
**Trading Recommendation:** BUY / SELL / HOLD / AVOID

**Key Takeaway:** [2-3 sentence summary of the most important finding]

**Biggest Catalyst:** [Most significant news/event affecting price]

**Primary Risk:** [Main downside risk to watch]

---

## 💰 Price & Market Data

### Current Market Status

| Metric | USD Value | KES Value | Change | Interpretation |
|--------|-----------|-----------|--------|----------------|
| **Price** | $X.XXXX | KSh X,XXX.XX | +X.XX% | |
| **24h High** | $X.XXXX | KSh X,XXX.XX | | Resistance |
| **24h Low** | $X.XXXX | KSh X,XXX.XX | | Support |
| **24h Volume** | $XXX M | KSh XXX B | +/- X% | High/Low activity |
| **5-min Avg** | $X.XXXX | KSh X,XXX.XX | | Current momentum |
| **Weighted Avg** | $X.XXXX | KSh X,XXX.XX | | Fair value |

### Price Performance

| Timeframe | Change | High USD | High KES | Low USD | Low KES | Trend |
|-----------|--------|----------|----------|---------|---------|-------|
| **1 Hour** | +X.XX% | $X.XX | KSh XXX | $X.XX | KSh XXX | 📈/📉 |
| **4 Hours** | +X.XX% | $X.XX | KSh XXX | $X.XX | KSh XXX | 📈/📉 |
| **24 Hours** | +X.XX% | $X.XX | KSh XXX | $X.XX | KSh XXX | 📈/📉 |
| **7 Days** | +X.XX% | $X.XX | KSh XXX | $X.XX | KSh XXX | 📈/📉 |
| **30 Days** | +X.XX% | $X.XX | KSh XXX | $X.XX | KSh XXX | 📈/📉 |

### Order Book Analysis

**Liquidity:** High / Medium / Low

**Top 10 Bids:**
- Cumulative: XXX {SYMBOL} (~$XXX,XXX)
- Strongest support: $X.XXXX (XXX {SYMBOL})

**Top 10 Asks:**
- Cumulative: XXX {SYMBOL} (~$XXX,XXX)
- Strongest resistance: $X.XXXX (XXX {SYMBOL})

**Bid/Ask Spread:** $X.XXXX (X.XX%) - Tight/Wide

**Interpretation:**
- [Analysis of buy vs sell pressure]
- [Support/resistance levels from order book]

---

## 📈 Multi-Timeframe Technical Analysis

### 1-Hour Chart (Short-Term)

| Indicator | Value | Signal | Interpretation |
|-----------|-------|--------|----------------|
| **RSI(14)** | XX.XX | Overbought/Neutral/Oversold | |
| **MACD** | X.XX / X.XX | Bullish/Bearish Crossover | |
| **Stochastic K/D** | XX / XX | Overbought/Oversold | |
| **CCI(20)** | XX.XX | Buy/Sell Zone | |
| **ADX** | XX.XX | Strong/Weak Trend | |
| **EMA 20** | $X.XXXX | Above/Below | Support/Resistance |
| **EMA 50** | $X.XXXX | Above/Below | Trend direction |
| **SMA 200** | $X.XXXX | Above/Below | Long-term trend |
| **Bollinger Bands** | Upper: $X.XX / Lower: $X.XX | Position | |
| **Recommendation** | BUY/SELL/NEUTRAL | Confidence: X% | |

**1h Interpretation:** [Detailed analysis of short-term setup]

### 4-Hour Chart (Medium-Term)

| Indicator | Value | Signal | Trend Confirmation |
|-----------|-------|--------|-------------------|
| **RSI(14)** | XX.XX | | |
| **MACD** | X.XX / X.XX | | |
| **EMA 20** | $X.XXXX | | |
| **EMA 50** | $X.XXXX | | |
| **Recommendation** | BUY/SELL/NEUTRAL | | |

**4h Interpretation:** [Medium-term trend analysis]

### Daily Chart (Long-Term)

| Indicator | Value | Signal | Major Trend |
|-----------|-------|--------|-------------|
| **RSI(14)** | XX.XX | | |
| **MACD** | X.XX / X.XX | | |
| **EMA 50** | $X.XXXX | | |
| **EMA 200** | $X.XXXX | | |
| **Recommendation** | BUY/SELL/NEUTRAL | | |

**Daily Interpretation:** [Long-term trend and major levels]

### Timeframe Confluence

**Bullish Signals:** [Count and list]
**Bearish Signals:** [Count and list]
**Conflicting Signals:** [Note any divergences between timeframes]

**Overall Technical Grade:** A+ / A / B / C / D / F

---

## 📰 News & Fundamental Analysis

### News Volume & Sentiment

**Total Articles (Last 24h):** XX articles
**Sentiment Breakdown:**
- 🟢 Bullish: XX articles (XX%)
- 🔴 Bearish: XX articles (XX%)
- 🟡 Neutral: XX articles (XX%)

**Overall News Sentiment Score:** X/10

### Top Headlines (Last 24 Hours)

**BULLISH NEWS:**
1. **[Headline]** - Source - [Time]
   - Impact: High/Medium/Low
   - Summary: [Key points]

2. **[Headline]** - Source - [Time]
   - Impact: High/Medium/Low
   - Summary: [Key points]

**BEARISH NEWS:**
1. **[Headline]** - Source - [Time]
   - Impact: High/Medium/Low
   - Summary: [Key points]

**NEUTRAL/INFORMATIONAL:**
1. **[Headline]** - Source - [Time]

### Key Catalysts & Narratives

**Primary Narrative:** [What's driving {SYMBOL} right now?]

**Catalysts Identified:**
1. [Catalyst 1] - Impact: High/Medium/Low - Timeframe: Immediate/Short/Long
2. [Catalyst 2] - Impact: High/Medium/Low - Timeframe: Immediate/Short/Long
3. [Catalyst 3] - Impact: High/Medium/Low - Timeframe: Immediate/Short/Long

**Upcoming Events:**
- [Event 1] - Date: [Date]
- [Event 2] - Date: [Date]

**Competitive Analysis:**
- How {SYMBOL} compares to competitors
- Market share / TVL / user metrics (if available)
- Unique value proposition

---

## 🐦 Social Sentiment Analysis

### Twitter Activity

**Mention Volume:** High / Medium / Low (Estimated XXX+ mentions/hour)

**Sentiment Breakdown:**
- 🟢 Bullish: XX%
- 🔴 Bearish: XX%
- 🟡 Neutral: XX%

**Overall Social Sentiment:** Extremely Bullish / Bullish / Neutral / Bearish / Extremely Bearish

### Trending Hashtags

1. #{SYMBOL} - Intensity: 🔥🔥🔥 / 🔥🔥 / 🔥
2. #{SYMBOL}Army / #{SYMBOL}Nation - Intensity:
3. [Other relevant hashtags]

### Community Sentiment Indicators

**FOMO Level:** 🚀🚀🚀 (10/10) → 😐 (1/10)
**Fear Level:** 😱😱😱 (10/10) → 😊 (1/10)

**Influencer Consensus:**
- Influencer X: [Bullish/Bearish] - "Quote"
- Influencer Y: [Bullish/Bearish] - "Quote"

**Price Predictions Seen:**
- Short-term (1-7 days): $X.XX - $X.XX
- Medium-term (1-3 months): $X.XX - $X.XX

**Common Narratives:**
- "Next 100x"
- "Undervalued gem"
- "Dead coin" / "Scam"
- [Other narratives]

---

## 💥 Liquidations Analysis

### {SYMBOL} Liquidation Data (Last 100 Total Events)

**{SYMBOL} Specific:**
- Total Liquidations: XX events
- Total Value: $XXX,XXX
- Long Liquidations: XX events (XX%) - $XXX,XXX
- Short Liquidations: XX events (XX%) - $XXX,XXX
- Largest Single: $XX,XXX ([Long/Short])

### Interpretation

**Dominant Side:** [Longs/Shorts] getting liquidated

**What This Means:**
- [If shorts liquidated]: Bearish traders forced to buy back → Bullish pressure
- [If longs liquidated]: Bullish traders forced to sell → Bearish pressure
- [If balanced]: Healthy two-sided market

**Liquidation Ranking:**
- {SYMBOL} is #XX in liquidation volume among all coins
- [High/Low] relative to other altcoins

**Recent Cascade Risk:** High / Medium / Low

**Interpretation:** [Overall conclusion from liquidation patterns]

---

## 🔄 Correlation & Sector Analysis

### Correlation to BTC/ETH

**vs BTC:**
- Correlation: High / Medium / Low / Inverse
- Performance: Outperforming / Underperforming BTC by X.XX%
- Beta: X.XX (X.XX× more/less volatile than BTC)

**vs ETH:**
- Correlation: High / Medium / Low / Inverse
- Performance: Outperforming / Underperforming ETH by X.XX%

**Interpretation:**
- [Is {SYMBOL} following BTC or moving independently?]
- [Market regime: Risk-on or Risk-off for {SYMBOL}?]

### Sector Comparison

**Sector:** [Meme Coin / Layer 2 / DeFi / AI / Gaming / Payment / etc.]

**Peer Performance (24h):**

| Coin | Price | 24h Change | Volume | Status |
|------|-------|------------|--------|--------|
| {SYMBOL} | $X.XX | +X.XX% | $XXM | **ANALYZING** |
| Peer 1 | $X.XX | +X.XX% | $XXM | Comparison |
| Peer 2 | $X.XX | +X.XX% | $XXM | Comparison |
| Peer 3 | $X.XX | +X.XX% | $XXM | Comparison |

**Sector Leader:** [Which coin leading?]
**Sector Laggard:** [Which coin lagging?]

**{SYMBOL} Sector Rank:** #X out of X

**Sector Narrative:** [What's driving the sector?]

**{SYMBOL} Competitive Edge:**
- [Advantage 1]
- [Advantage 2]

**{SYMBOL} Weaknesses vs Peers:**
- [Weakness 1]
- [Weakness 2]

---

## 🎯 Trading Opportunities & Signals

### Primary Trade Setup

**Trade Type:** LONG / SHORT / AVOID

**Timeframe:** Scalp (< 4h) / Day Trade (< 24h) / Swing (1-7 days) / Position (weeks)

**Entry Strategy:**
- **Ideal Entry:** $X.XXXX (KSh X,XXX.XX)
- **Aggressive Entry:** $X.XXXX (KSh X,XXX.XX) - current market
- **Conservative Entry:** $X.XXXX (KSh X,XXX.XX) - wait for pullback

**Targets:**
- **Target 1 (50% position):** $X.XXXX (KSh X,XXX.XX) - +X.XX%
- **Target 2 (30% position):** $X.XXXX (KSh X,XXX.XX) - +X.XX%
- **Target 3 (20% position):** $X.XXXX (KSh X,XXX.XX) - +X.XX%
- **Moon Target:** $X.XXXX (KSh X,XXX.XX) - +XX.XX%

**Stop Loss:**
- **Tight Stop:** $X.XXXX (KSh X,XXX.XX) - -X.XX%
- **Normal Stop:** $X.XXXX (KSh X,XXX.XX) - -X.XX%
- **Wide Stop:** $X.XXXX (KSh X,XXX.XX) - -X.XX%

**Risk/Reward Ratio:** X.XX:1

**Position Sizing Recommendation:**
- Conservative: X% of portfolio
- Moderate: X% of portfolio
- Aggressive: X% of portfolio

### Trade Rationale

**Why This Trade Works:**
1. [Technical reason - e.g., RSI oversold + bullish divergence]
2. [Fundamental reason - e.g., Major partnership announcement]
3. [Sentiment reason - e.g., Social buzz increasing, FOMO building]
4. [Liquidation reason - e.g., Shorts being squeezed]

**Confidence Level:** Very High / High / Medium / Low

**Expected Timeframe to Target:** [Hours/Days]

### Alternative Scenarios

**If Price Goes Against You:**
- [What to do if stop is hit]
- [Re-entry strategy]

**If Price Consolidates:**
- [How long to wait]
- [Invalidation level]

---

## 🚨 Risk Assessment

### Critical Risks (MUST KNOW)

**HIGHEST RISKS:**
1. **[Risk 1]** - Probability: High/Medium/Low - Impact: Severe/Major/Minor
   - Mitigation: [How to protect against this]

2. **[Risk 2]** - Probability: High/Medium/Low - Impact: Severe/Major/Minor
   - Mitigation: [How to protect against this]

3. **[Risk 3]** - Probability: High/Medium/Low - Impact: Severe/Major/Minor
   - Mitigation: [How to protect against this]

### Support & Resistance Levels (CRITICAL)

**SUPPORT LEVELS:**
- **S1 (Critical):** $X.XXXX (KSh X,XXX) - MUST HOLD or [consequence]
- **S2 (Strong):** $X.XXXX (KSh X,XXX) - Major support
- **S3 (Last Line):** $X.XXXX (KSh X,XXX) - Breakdown level

**RESISTANCE LEVELS:**
- **R1 (Immediate):** $X.XXXX (KSh X,XXX) - First target
- **R2 (Major):** $X.XXXX (KSh X,XXX) - Key resistance
- **R3 (Breakout):** $X.XXXX (KSh X,XXX) - Moon level

**Watch Levels:**
- Break below $X.XXXX = EXIT ALL LONGS
- Break above $X.XXXX = BREAKOUT CONFIRMED

### Red Flags 🚩

**Technical Red Flags:**
- [e.g., Bearish divergence on RSI]
- [e.g., Death cross forming]

**Fundamental Red Flags:**
- [e.g., Negative regulatory news]
- [e.g., Team selling tokens]

**Sentiment Red Flags:**
- [e.g., Extreme greed/FOMO = top signal]
- [e.g., Sudden social silence = abandonment]

### Green Flags 🟢

**Technical Green Flags:**
- [e.g., Golden cross]
- [e.g., Bullish breakout]

**Fundamental Green Flags:**
- [e.g., New partnership]
- [e.g., Product launch]

**Sentiment Green Flags:**
- [e.g., Institutional interest]
- [e.g., Community growth]

---

## 💎 Hidden Insights & Alpha

### Unique Observations

**What Most Traders Are Missing:**
- [Insight 1 that's not obvious]
- [Insight 2 from deep analysis]

**Contrarian Take:**
- [If sentiment differs from technicals/fundamentals]

**Insider Perspective:**
- [What the liquidations/order book tells us that news doesn't]

### Comparative Advantage

**Why {SYMBOL} vs Others:**
- [What makes this coin special right now]

**Why NOT {SYMBOL}:**
- [Honest assessment of weaknesses]

---

## 📅 Short-Term Outlook (Next 24-72 Hours)

**Base Case (60% Probability):**
- Price Range: $X.XX - $X.XX
- Expected: [Brief scenario]

**Bull Case (25% Probability):**
- Price Target: $X.XX+
- Trigger: [What would cause this]

**Bear Case (15% Probability):**
- Price Target: $X.XX-
- Trigger: [What would cause this]

**Key Events to Watch:**
- [Event 1] - Date/Time
- [Event 2] - Date/Time

**Critical Levels for Next 24h:**
- Bullish above: $X.XXXX
- Bearish below: $X.XXXX

---

## 📋 Final Verdict

### Summary Rating

| Category | Score | Grade |
|----------|-------|-------|
| **Technical** | X/10 | A-F |
| **Fundamental** | X/10 | A-F |
| **Sentiment** | X/10 | A-F |
| **Risk/Reward** | X/10 | A-F |
| **OVERALL** | X/10 | A-F |

### Recommendation

**ACTION:** 🟢 STRONG BUY / BUY / HOLD / SELL / 🔴 STRONG SELL / ⚠️ AVOID

**Best For:**
- [Day Traders / Swing Traders / Long-term Holders]
- [High Risk Tolerance / Medium Risk / Conservative]

**Bottom Line:**
[2-3 sentences with clear, actionable conclusion]

**TL;DR for Busy Traders:**
[One sentence: Should I buy this coin right now? Yes/No and why in 10 words]

---

## 📊 Data Sources & Quality

**Data Collected:**
- ✅ Binance Market Data (Price, Volume, Order Book, Klines)
- ✅ TradingView Technical Indicators (Multi-timeframe)
- ✅ Crypto News (XX articles analyzed)
- ✅ Twitter Sentiment (Estimated from timeline)
- ✅ Liquidations Data (Last 100 events)
- ✅ Sector Comparison (Peers analyzed)

**Data Quality:** Excellent / Good / Fair / Limited

**Analysis Timestamp:** [Exact time]
**Data Freshness:** Real-time / < 5 min old / < 15 min old

---

**Disclaimer:** This analysis is for informational purposes only and is not financial advice. Cryptocurrency trading is highly risky. Always do your own research, use proper risk management, and never invest more than you can afford to lose. Past performance does not guarantee future results.

---

## 📝 Markdown File Export

**CRITICAL: Save the complete markdown analysis to a file automatically.**

Use the Write tool to save the markdown report generated above to a file with this naming convention:

**File Name Format:** `{SYMBOL}-Deep-Analysis-{YYYY-MM-DD}.md`

**Examples:**
- `XRP-Deep-Analysis-2025-11-08.md`
- `DOGE-Deep-Analysis-2025-11-08.md`
- `PEPE-Deep-Analysis-2025-11-08.md`

**File Location:** Current working directory (where the command is run from)

**File Content:** The COMPLETE markdown report generated above (from "# 🔍 Deep Analysis: {SYMBOL}" to the disclaimer at the end)

**IMPORTANT Instructions:**
1. After completing the analysis and generating the markdown content, use the Write tool
2. Save to file: `{SYMBOL}-Deep-Analysis-{YYYY-MM-DD}.md`
3. Include ALL sections with dual USD/KES currency throughout
4. Confirm to user: "✅ Analysis saved to: {filename}"

**File should include:**
- All sections from the markdown report structure above
- Executive Summary
- Price & Market Data (with dual currency)
- Technical Analysis (multi-timeframe)
- News & Fundamental Analysis
- Social Sentiment Analysis
- Liquidations Analysis
- Correlation & Sector Analysis
- Trading Opportunities
- Risk Assessment
- Hidden Insights & Alpha
- Short-Term Outlook
- Final Verdict
- Data Sources & Quality
- Disclaimer

This markdown file can then be:
- Opened in any markdown viewer (VS Code, Obsidian, Typora, etc.)
- Converted to PDF using Pandoc or online tools
- Uploaded to Google Drive when storage is available
- Shared with others
- Kept for historical reference

---

## Execution Checklist

Before completing analysis, ensure:
- [ ] **FIRST:** Get USD/KES exchange rate using currency conversion MCP
- [ ] Symbol validated and normalized
- [ ] Binance market data collected (8+ tools)
- [ ] TradingView indicators retrieved (3 timeframes)
- [ ] Extensive news search completed (7+ queries)
- [ ] Twitter sentiment analyzed
- [ ] Liquidations filtered for {SYMBOL}
- [ ] Sector comparison completed
- [ ] **CONVERT:** All USD values to KES using exchange rate
- [ ] Support/resistance levels identified (both USD and KES)
- [ ] Trade setup with entry/target/stop calculated (both currencies)
- [ ] Risk assessment comprehensive
- [ ] Final recommendation clear and actionable
- [ ] Markdown report generated (with dual currency throughout)
- [ ] **SAVE:** Markdown file created: `{SYMBOL}-Deep-Analysis-{YYYY-MM-DD}.md`
- [ ] **VERIFY:** All prices display both USD and KES correctly
- [ ] **CONFIRM:** File saved successfully and location reported to user

---

**Now execute this comprehensive single-altcoin analysis for {SYMBOL}!**
