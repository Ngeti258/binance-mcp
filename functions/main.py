import logging
import os
import sys
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import functions_framework

# Ensure we can import local modules
# In Cloud Functions, files are in the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from trading_screener import get_trading_signals
    from binance_integration import get_binance_prices
    from trading_utils import generate_majors_report, setup_logging
except ImportError:
    # Fallback for local testing if files are in parent dir
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    from trading_screener import get_trading_signals
    from binance_integration import get_binance_prices
    from trading_utils import generate_majors_report, setup_logging

# Initialize Firebase
if not firebase_admin._apps:
    firebase_admin.initialize_app()

db = firestore.client()
logger = logging.getLogger(__name__)
setup_logging()

# List of Major Coins to Analyze
MAJOR_COINS = [
    "BINANCE:BTCUSDT",
    "BINANCE:ETHUSDT",
    "BINANCE:BNBUSDT",
    "BINANCE:SOLUSDT",
    "BINANCE:XRPUSDT",
    "BINANCE:ADAUSDT",
    "BINANCE:AVAXUSDT",
    "BINANCE:DOTUSDT",
    "BINANCE:MATICUSDT",
    "BINANCE:LINKUSDT",
    "BINANCE:UNIUSDT",
    "BINANCE:ATOMUSDT",
    "BINANCE:LTCUSDT",
    "BINANCE:TRXUSDT",
    "BINANCE:DOGEUSDT"
]

@functions_framework.cloud_event
def scheduled_analysis(cloud_event):
    """
    Triggered by a schedule (e.g., EventArc or Cloud Scheduler).
    Runs the majors analysis and saves the report to Firestore.
    """
    logger.info(f"Starting scheduled analysis at {datetime.now()}")
    
    try:
        # 1. Get Trading Signals
        logger.info("Fetching trading signals...")
        results = get_trading_signals(
            exchange="BINANCE",
            symbols=MAJOR_COINS,
            timeframe="4h"
        )
        
        if not results:
            logger.error("No results returned from screener.")
            return "Analysis failed: No results"

        # 2. Get Live Prices (for accuracy)
        logger.info("Fetching live prices...")
        try:
            prices = get_binance_prices(MAJOR_COINS)
        except Exception as e:
            logger.warning(f"Could not fetch live prices: {e}. Using screener prices.")
            prices = {}

        # 3. Generate Report
        logger.info("Generating report...")
        report_markdown = generate_majors_report(results, prices)
        
        # 4. Save to Firestore
        logger.info("Saving to Firestore...")
        doc_ref = db.collection("market_analysis").document()
        doc_ref.set({
            "content": report_markdown,
            "timestamp": firestore.SERVER_TIMESTAMP,
            "type": "majors_analysis",
            "status": "completed"
        })
        
        logger.info(f"Analysis completed and saved to document {doc_ref.id}")
        return f"Success: {doc_ref.id}"

    except Exception as e:
        logger.exception(f"Error during analysis: {e}")
        return f"Error: {e}"
