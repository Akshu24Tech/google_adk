# deploy/run_flow.py
import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

import vertexai
from vertexai import agent_engines

PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("LOCATION", "us-central1")
RESOURCE_ID = os.environ.get("RESOURCE_ID") # Set this after deployment

if not PROJECT_ID or not RESOURCE_ID:
    print("❌ ERROR: PROJECT_ID and RESOURCE_ID must be set in .env.")
    print("Get the RESOURCE_ID from the output of deploy.py")
    exit(1)

vertexai.init(project=PROJECT_ID, location=LOCATION)

print(f"🔗 Connecting to Remote Engine: {RESOURCE_ID}")
remote_engine = agent_engines.get(RESOURCE_ID)

user_id = "test_user_remote"
print("\n💬 Sending test message: 'What's the best way to save for a house?'")

try:
    # Query the remote engine
    for event in remote_engine.stream_query(
        user_id=user_id,
        message="What's the best way to save for a house?"
    ):
        # The remote engine returns events in a similar format to the local runner
        if 'content' in event and 'parts' in event['content']:
            for part in event['content']['parts']:
                if 'text' in part:
                    print(part['text'], end="", flush=True)
    print("\n\n✅ Remote query successful!")
except Exception as e:
    print(f"\n❌ Error during remote query: {e}")
