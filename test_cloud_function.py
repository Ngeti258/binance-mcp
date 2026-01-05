import sys
import os
import logging
from unittest.mock import MagicMock

# Mock firebase_admin before importing main
sys.modules['firebase_admin'] = MagicMock()
sys.modules['firebase_admin.credentials'] = MagicMock()
sys.modules['firebase_admin.firestore'] = MagicMock()

# Mock google.cloud and functions_framework
mock_ff = MagicMock()
# IMPORTANT: The decorator must return the function it decorates
mock_ff.cloud_event = lambda func: func
sys.modules['google.cloud'] = MagicMock()
sys.modules['google.cloud'].functions_framework = mock_ff
sys.modules['google.cloud.functions_framework'] = mock_ff

# Add functions directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'functions'))

from functions.main import scheduled_analysis

# Setup logging to see output
logging.basicConfig(level=logging.INFO)

print("🚀 Starting Dry Run of Cloud Function Logic...")
print("---------------------------------------------")

# Mock the database client
mock_db = MagicMock()
mock_collection = MagicMock()
mock_doc = MagicMock()
mock_db.collection.return_value = mock_collection
mock_collection.document.return_value = mock_doc
mock_doc.id = "TEST_DOCUMENT_ID"

# Inject mock db into main module
import functions.main
functions.main.db = mock_db

# Run the function
result = scheduled_analysis(None)

print("\n---------------------------------------------")
print(f"✅ Execution Result: {result}")
print(f"📄 Document ID: {mock_doc.id}")

# Verify what would have been saved
if mock_doc.set.called:
    args = mock_doc.set.call_args[0][0]
    print("\n💾 Data that would be saved to Firestore:")
    print(f"Type: {args.get('type')}")
    print(f"Status: {args.get('status')}")
    print(f"Content Length: {len(args.get('content', ''))} chars")
    print("\n--- Content Preview ---")
    print(args.get('content')[:500] + "...")
else:
    print("\n❌ Error: Firestore set() was not called!")
