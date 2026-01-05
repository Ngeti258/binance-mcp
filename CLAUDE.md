# CLAUDE.md - Repository Guide for Claude Code

> This guide provides essential context for Claude Code instances working in this repository.

## Project Overview

**Binance MCP Server** is a dual-purpose repository combining:

1. **TypeScript MCP Server**: A Model Context Protocol server providing comprehensive Binance API integration (trading, wallet, staking, mining, etc.)
2. **Python Trading Analysis System**: Automated cryptocurrency market analysis with TradingView integration and scheduled analysis capabilities

The repository integrates multiple MCP servers for a complete crypto trading and analysis ecosystem.

---

## Quick Start Commands

### TypeScript MCP Server

```bash
# Install dependencies
npm install

# Build the TypeScript server
npm run build

# Run tests
npm test

# Initialize/setup (interactive)
npm run init

# Build and initialize
npm run init:build

# Auto-publish (for maintainers)
npm run publish:auto
```

### Python Trading Analysis

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run automated analysis (one-time)
python automated_analysis.py

# Run with custom parameters
python automated_analysis.py --exchange BINANCE --timeframe 4h --symbols BTCUSDT,ETHUSDT

# Run with filters
python automated_analysis.py --min-signal STRONG_BUY --notify

# Windows scheduled analysis (uses Task Scheduler)
run-majors-analysis.bat
run-market-analysis.bat
run-hourly-analysis.bat
```

---

## Architecture Overview

### TypeScript MCP Server (`src/`)

**Entry Point**: `src/index.ts`

The server uses a modular tool registration pattern:

```typescript
// Main server setup
const server = new McpServer({
    name: "binance-mcp",
    version: "1.0.0"
});

// Register domain-specific tools
registerBinanceSpotTools(server);
registerBinanceAlgoTools(server);
registerBinanceSimpleEarnTools(server);
// ... 15+ tool categories
```

**Tool Organization** (`src/tools/`):
- Each Binance API domain has its own directory
- Each directory contains modular tool implementations
- Index files export registration functions
- Client configuration in `src/config/`

**Key Binance API Domains**:
1. **binance-spot** - Spot trading, market data, account info
2. **binance-algo** - Algorithmic trading (TWAP, VP for futures & spot)
3. **binance-wallet** - Wallet operations, deposits, withdrawals
4. **binance-staking** - ETH/SOL staking, rewards, redemption
5. **binance-simple-earn** - Flexible/fixed earn products
6. **binance-convert** - Token conversion with quotes
7. **binance-mining** - Mining pool management
8. **binance-vip-loan** - VIP loan operations
9. **binance-dual-investment** - Dual investment products
10. **binance-nft** - NFT transactions and history
11. **binance-pay** - Binance Pay integration
12. **binance-fiat** - Fiat deposit/withdrawal
13. **binance-c2c** - C2C trading history
14. **binance-copy-trading** - Futures copy trading
15. **binance-rebate** - Spot rebate history

**Build Output**: `build/` directory (TypeScript compiled to JS)

### Python Trading Analysis System

**Core Modules**:

1. **automated_analysis.py** - Main entry point for scheduled analysis
   - Configurable symbols, timeframes, exchanges
   - Supports filtering by signal strength
   - Outputs to `analysis_reports/` directory

2. **tradingview_screener.py** - TradingView API integration
   - Fetches technical indicators from TradingView screener
   - Multi-timeframe analysis support
   - Timeframe mapping and validation

3. **trading_metrics.py** - Technical analysis calculator
   - Combines indicators into trading signals
   - Computes: RSI, MACD, Bollinger Bands, ADX, CCI, Stochastic
   - Signal generation: STRONG_BUY, BUY, HOLD, SELL, STRONG_SELL

4. **trading_indicators.py** - Individual indicator calculations
   - Modular indicator implementations
   - Signal computation for each indicator
   - Configurable weights and thresholds

5. **trading_utils.py** - Utility functions
   - Logging setup
   - Full analysis orchestration
   - Helper functions

6. **trading_constants.py** - Configuration constants
   - Signal enums
   - Default weights
   - Indicator thresholds

7. **binance_integration.py** - Binance API wrapper
   - Direct Binance market data access
   - Complements MCP server integration

**Analysis Outputs**:
- Markdown reports with timestamp naming
- Format: `majors-analysis-{YYYY-MM-DD}-{HH-MM}.md`
- Includes dual currency (USD/KES) pricing

---

## MCP Server Integrations

The repository is configured to work with multiple MCP servers via `.mcp.json`:

### Available MCP Servers

1. **binance-mcp** (This repo)
   - Local build: `./build/index.js`
   - Requires: `BINANCE_API_KEY`, `BINANCE_API_SECRET`

2. **x-mcp-server** (Twitter/X integration)
   - Location: `C:\Users\ngeti\Downloads\x-mcp-server\build\index.js`
   - Provides social sentiment analysis

3. **currency-conversion** (Remote)
   - Remote server: `https://currency-mcp.wesbos.com/sse`
   - Real-time currency conversion

4. **tradingview** (Local Python)
   - Location: `./mcp-tradingview-server/.venv/Scripts/mcp-tradingview.exe`
   - Technical indicators from TradingView

5. **google-sheets** (Remote via uvx)
   - Service account authentication
   - Requires: `.serviceAccountKey.json`

6. **crypto-news** (Local Python)
   - Location: `./crypto-news-mcp/`
   - News sentiment analysis

7. **crypto-liquidations** (Local Python)
   - Location: `./crypto-liquidations-mcp/`
   - Real-time liquidation tracking

### MCP Integration Pattern

All MCP servers expose tools via the Model Context Protocol. Access patterns:

```javascript
// From Claude Code
mcp__binance-mcp__BinanceTickerPrice
mcp__tradingview__get_indicators
mcp__crypto-news__get_crypto_news
mcp__x-mcp-server__get-home-timeline
// etc.
```

---

## Claude Code Slash Commands

Located in `.claude/commands/`:

### `/majors` - Major Cryptocurrencies Analysis
- **File**: `.claude/commands/majors.md`
- **Purpose**: Comprehensive hourly analysis of top 15 major cryptos
- **Scope**: BTC, ETH, BNB, SOL, XRP, ADA, AVAX, DOT, MATIC, LINK, UNI, ATOM, LTC, TRX, DOGE
- **Output**: Detailed markdown report with dual currency (USD/KES)
- **Workflow**:
  1. Get USD to KES exchange rate
  2. Collect Binance market data for all 15 coins
  3. Fetch TradingView indicators (1h, 4h, 1d timeframes)
  4. Gather crypto news for each coin
  5. Analyze social sentiment via Twitter/X
  6. Collect liquidations data
  7. Perform technical and fundamental analysis
  8. Generate trading opportunities with risk management
  9. Save comprehensive report to timestamped file

### `/market-analysis` - Full Market Analysis
- **File**: `.claude/commands/market-analysis.md`
- Broader market analysis (likely includes small-caps)

### `/analyze` - Quick Analysis
- **File**: `.claude/commands/analyze.md`
- Rapid analysis for specific symbols/scenarios

### `/price` - Price Lookup
- **File**: `.claude/commands/price.md`
- Quick price information retrieval

### `/reload` - Reload Configuration
- **File**: `.claude/commands/reload.md`
- Reload MCP server configurations

---

## Important Workflows

### 1. Running Automated Crypto Analysis

**Scheduled via Windows Task Scheduler**:
- `run-majors-analysis.bat` - Major coins hourly
- `run-market-analysis.bat` - Full market analysis
- `run-hourly-analysis.bat` - Hourly routine
- `run_automated_analysis.bat` - Main automation script

**PowerShell Setup Scripts**:
- `setup-scheduler.ps1` - Configure single scheduler
- `setup-dual-scheduler.ps1` - Configure dual schedulers
- `disable-lag-tasks.ps1` - Disable resource-intensive tasks

### 2. Building and Deploying MCP Server

```bash
# 1. Make code changes in src/
# 2. Build
npm run build

# 3. Test locally
npm test

# 4. Update .mcp.json with correct paths
# 5. Restart Claude Desktop to load changes
```

### 3. Adding New Binance API Tools

1. Create tool file in appropriate `src/tools/binance-*/` directory
2. Export tool from domain's `index.ts`
3. Register in main `src/index.ts`
4. Rebuild with `npm run build`
5. Tool becomes available as `mcp__binance-mcp__ToolName`

### 4. Customizing Trading Analysis

**Modify Analysis Parameters**:
- Edit `DEFAULT_SYMBOLS` in `automated_analysis.py`
- Adjust `DEFAULT_TIMEFRAME` for different intervals
- Customize `ALERT_SIGNALS` for notification triggers

**Add Custom Indicators**:
- Implement in `trading_indicators.py`
- Integrate in `trading_metrics.py`
- Update weights in `trading_constants.py`

---

## Key Configuration Files

### TypeScript Configuration

**tsconfig.json**:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true
  }
}
```

**package.json**:
- Name: `binance-mcp`
- Version: `1.0.8`
- Type: `module` (ES modules)
- Main: `index.js`
- Bin: `./build/index.js` (executable)

### Python Configuration

**requirements.txt**:
- tradingview-screener >= 1.0.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- ta >= 0.11.0 (technical analysis)
- requests >= 2.31.0

### Environment Variables

**.env** (Required for Binance):
```bash
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

**MCP Server Env** (Configured in `.mcp.json`):
- Binance: API keys
- Twitter/X: OAuth credentials
- Google Sheets: Service account path
- Crypto News: API key

---

## Common Development Patterns

### 1. Error Handling in TypeScript Tools

```typescript
// Standard pattern used throughout src/tools/
try {
    const response = await client.someApiCall(params);
    return { success: true, data: response };
} catch (error: any) {
    return {
        success: false,
        error: error.message || 'Unknown error'
    };
}
```

### 2. Tool Registration Pattern

```typescript
// src/tools/binance-domain/index.ts
export function registerDomainTools(server: McpServer) {
    server.addTool({
        name: "BinanceToolName",
        description: "What this tool does",
        schema: { /* Zod schema */ },
        handler: async (params) => { /* implementation */ }
    });
}
```

### 3. Python Analysis Workflow

```python
# Standard flow in automated_analysis.py
def run_analysis():
    # 1. Fetch indicators from TradingView
    indicators = fetch_screener_indicators(symbol, exchange, timeframe)

    # 2. Map to metrics format
    metrics_data = map_to_trading_metrics_format(indicators)

    # 3. Compute trading metrics
    metrics = compute_metrics(metrics_data)

    # 4. Get full analysis
    analysis = get_full_analysis(symbol, exchange, timeframe)

    # 5. Generate report
    save_report(analysis)
```

### 4. Dual Currency Display Pattern

```python
# Applied throughout major coins analysis
def format_price(usd_value, usd_to_kes_rate):
    kes_value = usd_value * usd_to_kes_rate
    return f"${usd_value:,.2f} (KSh {kes_value:,.2f})"
```

---

## Testing and Validation

### TypeScript Tests

```bash
npm test  # Runs test/testServer.js
```

**Test Location**: `test/testServer.js`

### Python Validation

```python
# In trading_screener.py
validate_indicator_data(indicators)  # Ensures data quality

# In trading_metrics.py
validate_indicators(indicators)  # Checks required fields
```

---

## Important Notes for Claude Code Instances

### When Working with Trading Analysis

1. **Always get USD to KES rate first** - Required for dual currency display
2. **Major coins only** - Focus on top 15 by market cap, exclude small-caps
3. **Save reports with timestamps** - Format: `majors-analysis-{YYYY-MM-DD}-{HH-MM}.md`
4. **Use parallel API calls** - MCP tools support concurrent requests
5. **Handle API failures gracefully** - Use fallback data when APIs rate limit

### When Modifying MCP Server

1. **TypeScript strict mode enabled** - All code must pass strict type checking
2. **ES modules required** - Use `import/export`, not `require()`
3. **Build before testing** - Always run `npm run build` after changes
4. **Update version** - Increment package.json version for releases
5. **Test with Claude Desktop** - Restart Claude Desktop to load changes

### When Adding New Features

1. **Follow modular pattern** - Keep tools in separate files by domain
2. **Document slash commands** - Add `.md` files to `.claude/commands/`
3. **Update README** - Keep main README.md in sync with features
4. **Add type safety** - Use Zod schemas for tool parameters
5. **Consider MCP integration** - Can this be an external MCP server?

### Security Considerations

1. **Never commit API keys** - Use .env files (gitignored)
2. **Binance API restrictions** - Configure IP whitelist in Binance settings
3. **Service account security** - Protect `.serviceAccountKey.json`
4. **Rate limiting** - Implement backoff for API calls
5. **Validate all inputs** - Sanitize user-provided parameters

---

## Troubleshooting Common Issues

### MCP Server Not Loading

1. Check `.mcp.json` paths are absolute and correct
2. Ensure `npm run build` completed successfully
3. Verify environment variables in `.mcp.json`
4. Restart Claude Desktop completely
5. Check Claude Desktop logs

### Python Import Errors

```bash
# Ensure virtual environment activated (if using)
pip install -r requirements.txt

# Or install individual package
pip install tradingview-screener
```

### Binance API Errors

- **403 Forbidden**: Check API key/secret in `.env`
- **418 IP Ban**: Rate limited, implement backoff
- **-1021 Timestamp**: System clock sync issue
- **-2010 Insufficient Balance**: Account balance too low

### TradingView Data Issues

- **Failed indicators**: Symbol may not exist on exchange
- **Empty response**: Check symbol format (BTCUSD not BTC/USD)
- **Stale data**: Verify exchange parameter matches symbol

---

## Repository Maintenance

### File Cleanup

Generated files that can accumulate:
- `majors-analysis-*.md` - Analysis reports
- `market-analysis-*.md` - Market reports
- `analysis_reports/` - Python analysis outputs
- `automation.log` - Automation logs

### Dependencies Updates

```bash
# TypeScript
npm update
npm audit fix

# Python
pip install --upgrade -r requirements.txt
```

### Git Workflow

**Current Branch**: `main`

**Untracked Files** (consider .gitignore):
- `.claude/` - Local Claude Code config
- `.mcp.json` - Contains API keys
- `.serviceAccountKey.json` - Google service account
- `*-analysis-*.md` - Generated reports
- `*.log` - Log files
- `__pycache__/` - Python cache
- `crypto-*-mcp/` - Nested MCP servers
- `mcp-tradingview-server/` - Nested MCP server

---

## Additional Resources

### Official Documentation

- **Binance API**: https://developers.binance.com/
- **Model Context Protocol**: https://modelcontextprotocol.io/
- **TradingView**: https://www.tradingview.com/

### Related Projects

- MCP servers in subdirectories:
  - `crypto-news-mcp/` - News sentiment MCP server
  - `crypto-liquidations-mcp/` - Liquidations tracking
  - `mcp-tradingview-server/` - TradingView integration

### Example Usage Guides

- `README.md` - Main project README
- `SETUP_GUIDE.md` - Setup instructions
- `COMMANDS-REFERENCE.md` - Command reference
- `COMPLETE_SYSTEM_GUIDE.md` - System overview
- `Crypto-Trading-Complete-Guide.md` - Trading guide

---

## Summary for Quick Reference

**To analyze major cryptocurrencies**: Use `/majors` slash command
**To build MCP server**: `npm run build`
**To test changes**: `npm test`
**To add new Binance tool**: Create in `src/tools/binance-*/`, register in index
**To run Python analysis**: `python automated_analysis.py`
**To schedule analysis**: Use batch files with Windows Task Scheduler

**Key Files to Know**:
- `src/index.ts` - MCP server entry point
- `automated_analysis.py` - Python analysis entry
- `.mcp.json` - MCP servers configuration
- `.claude/commands/majors.md` - Major coins analysis prompt
- `package.json` - NPM scripts and dependencies
- `requirements.txt` - Python dependencies

---

*Last Updated: 2025-12-06*
*Repository: binance-mcp*
*For Claude Code v1.x*
