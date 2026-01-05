# Price Command

Get the current price of a cryptocurrency in Kenyan Shillings (KES).

## Usage
User will provide: /price <asset>

Example: /price bitcoin

## Instructions

1. Map the asset name to its Binance trading symbol:
   - bitcoin -> BTCUSDT
   - ethereum -> ETHUSDT
   - bnb -> BNBUSDT
   - solana -> SOLUSDT
   - cardano -> ADAUSDT
   - ripple -> XRPUSDT
   - dogecoin -> DOGEUSDT
   - polkadot -> DOTUSDT
   - avalanche -> AVAXUSDT
   - chainlink -> LINKUSDT
   - litecoin -> LTCUSDT
   - If the asset name is not in the list, try appending "USDT" to the uppercase asset name (e.g., "pepe" -> "PEPEUSDT")

2. Use the Binance MCP tool `mcp__binance-mcp__BinanceTickerPrice` with the mapped symbol to get the current price in USDT

3. Use the currency converter MCP tool `convert_currency` to convert from USD to KES:
   - from: "USD"
   - to: "KES"
   - amount: the price from step 2

4. Display the result in a clear format showing:
   - The cryptocurrency name and symbol
   - Current price in USDT
   - Converted price in KES (formatted with commas for readability)
   - Timestamp of the price

Example output format:
```
Bitcoin (BTC)
💵 $102,545.15 USDT
🇰🇪 13,228,370 KES

Price as of [timestamp]
```

If there's an error (invalid symbol, API failure, etc.), provide a helpful error message.
