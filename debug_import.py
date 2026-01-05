import sys
import traceback

print(f"Python Executable: {sys.executable}")
print(f"Python Path: {sys.path}")

try:
    print("Attempting to import tradingview_screener...")
    import tradingview_screener
    print(f"✅ Successfully imported tradingview_screener from {tradingview_screener.__file__}")
    
    from tradingview_screener import Query
    print("✅ Successfully imported Query")
    
except ImportError:
    print("❌ ImportError occurred:")
    traceback.print_exc()
except Exception:
    print("❌ An unexpected error occurred during import:")
    traceback.print_exc()
