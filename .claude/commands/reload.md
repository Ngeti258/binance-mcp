# Reload Command

Reload MCP server configurations by restarting the Claude Code session.

## Usage
User will provide: /reload

## Instructions

**Important Note:** Claude Code does not have a built-in mechanism to hot-reload MCP server configurations while a session is running. MCP servers are initialized when the session starts by reading the `.mcp.json` configuration file.

When the user runs this command:

1. Inform the user that to reload MCP configurations, they need to restart their Claude Code session

2. Provide clear instructions:
   ```
   To reload MCP server configurations:

   Option 1: Exit and restart
   - Close this Claude Code session
   - Start a new session in the same directory

   Option 2: Use the keyboard shortcut
   - Press Ctrl+C to exit (or Cmd+C on Mac)
   - Restart Claude Code in your terminal

   After restarting, run /mcp to verify all servers are loaded.
   ```

3. Before they restart, show them:
   - Current MCP servers in `.mcp.json` by reading the file
   - A summary of what will be loaded after restart

4. Optionally validate the `.mcp.json` syntax to catch any errors before they restart:
   - Read the `.mcp.json` file
   - Parse it as JSON to verify it's valid
   - Report any syntax errors if found
   - List all configured MCP servers

Example output format:
```
📋 Current MCP Configuration in .mcp.json:

✓ binance-mcp (node)
✓ x-mcp-server (node)
✓ currency-conversion (npx remote)
✓ tradingview (Python executable)
✓ google-sheets (uvx)

Total: 5 MCP servers configured

✅ Configuration file is valid JSON

To apply these changes, please restart your Claude Code session:
- Press Ctrl+C to exit
- Run `claude` again to start a new session
```

If there are JSON syntax errors:
```
❌ Error: Invalid JSON in .mcp.json
Line 15: Unexpected token ','

Please fix the syntax error before restarting.
```
