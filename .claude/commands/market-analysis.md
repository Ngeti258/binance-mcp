# Hourly ALTCOIN-Focused Crypto Market Analysis Command

You are performing an independent hourly cryptocurrency market analysis with **90% FOCUS ON ALTCOINS**. Each analysis should be comprehensive and stored separately without reference to previous hours.

## Analysis Framework

**IMPORTANT:**
- **90% of analysis = ALTCOINS** (trending coins, emerging narratives, altcoin-specific patterns)
- **10% of analysis = BTC/ETH context** (only for market reference)
- Prioritize discovering trending altcoins from news, Twitter, and liquidations
- Focus on coins showing unusual activity, volume spikes, or social buzz

---

## PHASE 1: Discover Trending Altcoins (CRITICAL)

### 1A. News-Based Altcoin Discovery
Use `mcp__crypto-news__get_latest_news` and `mcp__crypto-news__get_crypto_news` extensively:

**Search Queries (run all in parallel):**
- "altcoin" (max_pages: 3)
- "altseason" (max_pages: 2)
- "100x" (max_pages: 2)
- "meme coin" (max_pages: 2)
- "new listing" (max_pages: 2)
- "pump" (max_pages: 2)
- "trending crypto" (max_pages: 2)
- "solana ecosystem" (max_pages: 2)
- "layer 2" (max_pages: 2)
- "defi" (max_pages: 2)
- "NFT" (max_pages: 1)
- "AI crypto" (max_pages: 2)
- "gaming token" (max_pages: 1)

**From news, extract:**
- All mentioned altcoin symbols (XRP, ADA, DOGE, SHIB, PEPE, etc.)
- Performance percentages mentioned
- Trending narratives (AI, gaming, layer 2, memes, etc.)
- New project launches or listings
- Partnership announcements

### 1B. Twitter Trending Altcoin Discovery
Use X MCP tools extensively:

- `mcp__x-mcp-server__get-home-timeline` (maxResults: 10) - Avoid rate limits
- Look for mentions of altcoins in timeline
- Identify trending hashtags: #altseason, #memecoin, #crypto, etc.
- Find which coins are being discussed most

### 1C. Liquidations-Based Altcoin Discovery
Use `mcp__crypto-liquidations__get_latest_liquidations` (limit: 100):

**Analyze liquidations data for:**
- Which altcoins had most liquidation events
- Which symbols show unusual liquidation activity
- Altcoins with heaviest dollar liquidations
- New coins appearing in liquidations (sign of trading interest)

**Create TRENDING ALTCOINS LIST:**
Based on news + Twitter + liquidations, compile top 15-20 altcoins showing:
- Most news mentions
- Highest social buzz
- Unusual liquidation activity
- Biggest % gainers mentioned
- New narratives emerging

---

## PHASE 2: Deep Altcoin Market Data Collection

### 2A. Binance Altcoin Data Collection
For **EACH altcoin** in trending list, collect:

Use these tools in parallel for top 15-20 altcoins:
- `mcp__binance-mcp__BinanceTickerPrice` - Current price
- `mcp__binance-mcp__BinanceTicker24hr` - 24h stats (volume, change %, high/low)
- `mcp__binance-mcp__BinanceDepth` (limit: 100) - Order book liquidity
- `mcp__binance-mcp__BinanceKlines` (interval: 1h, limit: 24) - Hourly candles
- `mcp__binance-mcp__BinanceAvgPrice` - 5-min average

**Priority Altcoins to ALWAYS check:**
1. XRPUSDT, ADAUSDT, DOGEUSDT, SHIBUSDT
2. AVAXUSDT, DOTUSDT, LINKUSDT, ATOMUSDT
3. ARBUSDT, OPUSDT, MATICUSDT (Layer 2s)
4. UNIUSDT, AAVEUSDT, MKRUSDT (DeFi)
5. PEPEUSDT, FLOKIUSDT, BONKUSDT (Memes)
6. APTUSDT, SUIUSDT, SEIUSDT (New Layer 1s)
7. Plus ANY coins trending from Phase 1

**BTC/ETH Context (10% focus only):**
- Only collect basic data: price, 24h change, volume
- Use as market reference point
- Don't do deep technical analysis

### 2B. TradingView Altcoin Technical Analysis
For top 10-15 trending altcoins, get full indicators:

Use `mcp__tradingview__get_indicators`:
- Symbols: Top trending altcoins (e.g., XRPUSD, ADAUSD, DOGEUSD, etc.)
- Exchange: BINANCE
- Timeframe: 1h
- all_indicators: true

**Focus on:**
- RSI (overbought/oversold)
- MACD momentum
- Volume patterns
- Recommendation signals
- Relative strength vs BTC

**BTC/ETH:** Only basic indicators for context

---

## PHASE 3: Altcoin-Specific Analysis

### 3A. Altcoin Liquidations Deep Dive
Analyze 100+ recent liquidations:

**Count by Symbol:**
- How many liquidations per altcoin?
- Long vs short ratio per altcoin
- Dollar value liquidated per altcoin
- Cascade risk assessment

**Identify:**
- Which altcoins getting squeezed (high short liq %)
- Which altcoins longs getting wrecked (high long liq %)
- New altcoins appearing in liquidations
- Unusual patterns (sudden spike in liquidations)

### 3B. Altcoin News Narrative Analysis
**Categorize all altcoin news by theme:**

1. **Meme Coin Mania:** DOGE, SHIB, PEPE, BONK, FLOKI, etc.
   - Sentiment, hype level, Elon tweets?

2. **Layer 2 Surge:** ARB, OP, MATIC, ZK, etc.
   - Ethereum scaling narrative

3. **New Layer 1s:** APT, SUI, SEI, HBAR, etc.
   - Competition to ETH/SOL

4. **DeFi Renaissance:** UNI, AAVE, MKR, COMP, etc.
   - TVL changes, protocol news

5. **AI Narrative:** FET, AGIX, RNDR, etc.
   - AI + crypto crossover hype

6. **Gaming/Metaverse:** SAND, MANA, AXS, IMX, etc.
   - Gaming adoption news

7. **Real World Assets:** ONDO, MKR, etc.
   - Tokenization trends

8. **XRP/Regulatory:** XRP-specific (ETF, Ripple case, etc.)

**For EACH category:**
- Count of news articles
- Overall sentiment (bullish/bearish)
- Key catalysts mentioned
- Price impact correlation

### 3C. Twitter Altcoin Sentiment
**Analyze social buzz by category:**

From timeline and trending topics:
- Which altcoins mentioned most?
- Sentiment (bullish/bearish/FOMO)
- Influencer picks
- Community excitement level
- New narratives emerging

**Look for:**
- "100x gem" mentions
- "Next $COIN" comparisons
- FOMO indicators
- Fear indicators
- Shilling patterns

---

## PHASE 4: Altcoin Correlation Analysis

### 4A. Altcoin vs BTC Correlation
**Analyze:**
- Which altcoins moving WITH BTC (correlation)
- Which altcoins moving AGAINST BTC (divergence)
- Which altcoins outperforming BTC
- Which altcoins underperforming BTC

### 4B. Sector Rotation Analysis
**Identify capital flows:**
- Money rotating from BTC → Alts?
- Money rotating from ETH → Alts?
- Which altcoin sectors gaining (memes, L2s, DeFi, AI)?
- Which sectors bleeding?

### 4C. Altcoin Dominance Patterns
- Total altcoin market cap trends
- BTC dominance falling = altseason signal
- Which coins leading the alt rally?

---

## Output Format: ALTCOIN-FOCUSED REPORT

Create comprehensive markdown report:

### Executive Summary (Focus on Altcoins!)
- **Altcoin Market Phase:** Bull/Bear/Rotation/Mania
- **Top Performing Altcoin Sector:** (Memes/L2/DeFi/AI/etc.)
- **Hottest Altcoins This Hour:** (Top 5 by volume/news/social buzz)
- **Altcoin Narrative:** What's trending in altcoin space?
- BTC/ETH: Brief 2-sentence context only

### 🔥 TRENDING ALTCOINS (Top 20)

| Rank | Symbol | Current Price | 24h % | 24h Volume | News Mentions | Twitter Buzz | Liquidations | Trend |
|------|--------|---------------|-------|------------|---------------|--------------|--------------|-------|
| 1 | XRP | $X.XX | +X.X% | $XXM | High | 🔥🔥🔥 | XX events | 🚀 |
| 2 | DOGE | $X.XX | +X.X% | $XXM | Med | 🔥🔥 | XX events | 📈 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

### 📊 ALTCOIN SECTOR PERFORMANCE

**Meme Coins:**
- DOGE: $X.XX (+X.X%), Volume $XXM
- SHIB: $X.XX (+X.X%), Volume $XXM
- PEPE: $X.XX (+X.X%), Volume $XXM
- **Sector Sentiment:** Bullish/Bearish/Neutral
- **News Count:** XX articles
- **Key Catalyst:** [Main news driving sector]

**Layer 2 Tokens:**
- ARB: $X.XX (+X.X%), Volume $XXM
- OP: $X.XX (+X.X%), Volume $XXM
- **Sector Sentiment:**
- **Key Catalyst:**

**New Layer 1s:**
- APT, SUI, SEI data and analysis

**DeFi Tokens:**
- UNI, AAVE, MKR data

**AI Tokens:**
- FET, AGIX, RNDR data

**Gaming/Metaverse:**
- SAND, MANA, AXS data

**[Other Trending Sectors]:**
- Identify and analyze any emerging categories

### 📰 ALTCOIN NEWS ANALYSIS

**Top 10 Altcoin Headlines:**
1. [Headline] - **Symbol:** XRP - **Sentiment:** Bullish - **Impact:** High
2. [Headline] - **Symbol:** DOGE - **Sentiment:** Bearish - **Impact:** Medium
3. ...

**News Breakdown by Category:**
- Meme Coins: XX articles (Bullish: X, Bearish: X)
- Layer 2: XX articles (Bullish: X, Bearish: X)
- DeFi: XX articles
- AI: XX articles
- Gaming: XX articles

**Hottest Narratives:**
1. [Narrative 1] - Affecting [symbols]
2. [Narrative 2] - Affecting [symbols]

### 🐦 ALTCOIN SOCIAL SENTIMENT

**Most Mentioned Altcoins:**
1. $XRP - XXX mentions - Sentiment: Bullish/Bearish
2. $DOGE - XXX mentions - Sentiment: Bullish/Bearish
3. ...

**Trending Hashtags:**
- #altseason - Intensity: High/Med/Low
- #memecoin - Intensity:
- #100x - Intensity:

**Influencer Picks:**
- Influencer X is bullish on: [coins]
- Influencer Y is bearish on: [coins]

**FOMO Meter:** [Scale 1-10]
**Fear Meter:** [Scale 1-10]

### 💥 ALTCOIN LIQUIDATIONS ANALYSIS

**Top Liquidated Altcoins (Last 100 Events):**

| Symbol | Total Liq | Long Liq % | Short Liq % | Largest Liq | Interpretation |
|--------|-----------|------------|-------------|-------------|----------------|
| TRUTH | $XXk | XX% | XX% | $XXk | Short squeeze |
| XRP | $XXk | XX% | XX% | $XXk | ... |

**Liquidation Hotspots:**
- [Symbol]: Heavy shorts liquidated = bullish squeeze
- [Symbol]: Heavy longs liquidated = bearish pressure

**New Coins in Liquidations:**
- [List new symbols appearing - trading interest indicator]

### 📈 ALTCOIN TECHNICAL ANALYSIS

**Top 10 Altcoins Technical Summary:**

| Symbol | RSI | MACD | Recommend | Support | Resistance | Signal |
|--------|-----|------|-----------|---------|------------|--------|
| XRP | XX | Bullish | BUY | $X.XX | $X.XX | 🟢 |
| DOGE | XX | Bearish | SELL | $X.XX | $X.XX | 🔴 |

**Oversold Altcoins (RSI < 30):**
- [List] - Potential bounce candidates

**Overbought Altcoins (RSI > 70):**
- [List] - Potential pullback risk

**Bullish Momentum (MACD Positive):**
- [List with recommendations]

### 🔄 ALTCOIN ROTATION ANALYSIS

**Capital Flow Patterns:**
- BTC → Alts: [Yes/No] - Evidence: [volume, correlation]
- ETH → Alts: [Yes/No]
- Large Cap Alts → Small Cap: [Yes/No]

**Winning Sectors:**
1. [Sector] - Average +X.X%
2. [Sector] - Average +X.X%

**Losing Sectors:**
1. [Sector] - Average -X.X%

**Sector Rotation Prediction:**
- Money flowing INTO: [sectors]
- Money flowing OUT OF: [sectors]

### 💎 HIDDEN GEMS (Low Volume, High Potential)

**Altcoins with:**
- Low news mentions BUT strong technicals
- Low social buzz BUT rising volume
- Undervalued vs sector peers

[List 3-5 potential "hidden gems" with rationale]

### 🚨 ALTCOIN RISK ALERTS

**High Risk Altcoins:**
1. [Symbol] - Reason: Overbought + negative news
2. [Symbol] - Reason: Heavy long liquidations
3. [Symbol] - Reason: Broken support

**Avoid These:**
- [List with reasons]

### 🎯 ALTCOIN TRADING OPPORTUNITIES

**Best Altcoin Longs (Next 1-4 hours):**
1. **Symbol:** [COIN]
   - **Entry:** $X.XX
   - **Target:** $X.XX (+X%)
   - **Stop:** $X.XX
   - **Rationale:** [News catalyst + technical setup + social buzz]
   - **Risk/Reward:** X:1

2. [Repeat for top 5 opportunities]

**Best Altcoin Shorts:**
[If bearish setups exist]

**Swing Trade Setups:**
[Medium-term altcoin plays]

### BTC/ETH Context (Brief - 10% focus)

**BTC:** $XXX,XXX (+X.XX%) - [One sentence summary]
**ETH:** $X,XXX (+X.XX%) - [One sentence summary]
**Impact on Alts:** [How BTC/ETH affecting altcoin market]

---

## Currency Conversion (Kenyan Shillings)

**CRITICAL STEP - Must do before creating Sheets/Docs:**

Use Currency Conversion MCP to get current USD to KES exchange rate:

**Use `mcp__currency-conversion__get_latest_rates`:**
- base: "USD"
- symbols: "KES"

This returns the current USD/KES exchange rate (e.g., 1 USD = 129.50 KES)

**Store this rate as:** `USD_TO_KES`

**For ALL price/volume/liquidation values:**
1. Keep USD value
2. Calculate KES value: USD_value × USD_TO_KES
3. Display BOTH in reports:
   - Format: `$1,234 (KSh 159,843)`
   - Or in tables: `$1,234 | KSh 159,843`

**Currency Display Format:**
- USD: Use $ symbol, comma separators (e.g., $1,234.56)
- KES: Use KSh or Ksh, comma separators (e.g., KSh 159,843.20)

**Apply conversion to:**
- All coin prices (BTC, ETH, altcoins)
- All volumes (24h volume, etc.)
- All liquidation amounts
- All trading targets (entry, stop, targets)
- All market cap values
- All portfolio values

**Example Conversions:**
- BTC $102,000 → $102,000 (KSh 13,209,000)
- Volume $2.3B → $2.3B (KSh 297.85B)
- Entry $1.50 → $1.50 (KSh 194.25)

---

## 📝 Markdown File Export

**CRITICAL: Save the complete market analysis to a markdown file automatically.**

Use the Write tool to save the analysis report to a file with this naming convention:

**File Name Format:** `market-analysis-{YYYY-MM-DD}-{HH-MM}.md`

**Examples:**
- `market-analysis-2025-11-08-14-00.md`
- `market-analysis-2025-11-08-15-00.md`
- `market-analysis-2025-11-09-09-00.md`

**File Location:** Current working directory (where the command is run from)

**File Content:** The COMPLETE markdown report with all sections listed above

**IMPORTANT Instructions:**
1. After completing the analysis and generating the markdown content, use the Write tool
2. Save to file: `market-analysis-{YYYY-MM-DD}-{HH-MM}.md` (use current UTC time)
3. Include ALL sections with dual USD/KES currency throughout
4. Confirm to user: "✅ Market analysis saved to: market-analysis-{date}-{time}.md"

**File should include ALL sections:**
- Executive Summary (90% altcoin focus)
- 🔥 Trending Altcoins (Top 20 table with dual currency)
- 📊 Altcoin Sector Performance (all sectors with USD/KES prices)
- 📰 Altcoin News Analysis
- 🐦 Altcoin Social Sentiment
- 💥 Altcoin Liquidations Analysis (amounts in both currencies)
- 📈 Altcoin Technical Analysis (support/resistance in both currencies)
- 🔄 Altcoin Rotation Analysis
- 💎 Hidden Gems
- 🚨 Altcoin Risk Alerts
- 🎯 Altcoin Trading Opportunities (entry/target/stop in both currencies)
- BTC/ETH Context (brief, 10% focus)
- Full disclaimer

This markdown file can then be:
- Opened in any markdown viewer (VS Code, Obsidian, Typora, etc.)
- Converted to PDF using Pandoc or online tools
- Uploaded to Google Drive when storage is available
- Shared with team members
- Used for historical tracking of hourly analyses

---

## Execution Checklist

- [ ] **FIRST:** Get USD/KES exchange rate using currency conversion MCP
- [ ] Phase 1: Discovered 15-20 trending altcoins from news/Twitter/liquidations
- [ ] Phase 2: Collected Binance data for all trending altcoins
- [ ] Phase 2: Collected TradingView indicators for top 10 altcoins
- [ ] Phase 3A: Analyzed altcoin liquidations in detail
- [ ] Phase 3B: Categorized altcoin news by sector/narrative
- [ ] Phase 3C: Analyzed Twitter altcoin sentiment
- [ ] Phase 4: Performed correlation and rotation analysis
- [ ] **CONVERT:** All USD values to KES using exchange rate
- [ ] Created comprehensive altcoin-focused markdown report (90% altcoins) with dual currency
- [ ] **SAVE:** Markdown file created: `market-analysis-{YYYY-MM-DD}-{HH-MM}.md`
- [ ] Identified top 5 altcoin trading opportunities (entry/target/stop in both currencies)
- [ ] Flagged high-risk altcoins to avoid
- [ ] **VERIFY:** All prices display both USD and KES correctly
- [ ] **CONFIRM:** File saved successfully and location reported to user

---

## Important Notes

**ALTCOIN FOCUS = 90%:**
- Spend most time on altcoin discovery, analysis, and opportunities
- BTC/ETH are context only (10%)
- Prioritize emerging narratives and trending coins
- Look for "hidden gems" and sector rotation
- Track meme coin mania vs fundamental plays

**Data Sources Priority:**
1. News mentions = Discover what's trending
2. Twitter buzz = Gauge community sentiment
3. Liquidations = Find where action is happening
4. Binance data = Confirm with price/volume
5. TradingView = Technical entry/exit points

**Thoroughness:**
- Check 20+ altcoins minimum
- Analyze multiple sectors (memes, L2, DeFi, AI, gaming, etc.)
- Cross-reference news + social + technical
- Identify rotation patterns
- Provide specific trade setups

**Now execute this ALTCOIN-FOCUSED comprehensive market analysis!**
