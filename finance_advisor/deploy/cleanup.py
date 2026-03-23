# deploy/cleanup.py
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

if not PROJECT_ID:
    print("❌ ERROR: PROJECT_ID must be set in .env for cleanup.")
    exit(1)

vertexai.init(project=PROJECT_ID, location=LOCATION)

def list_deployments():
    print(f"🔍 Searching for deployments in {PROJECT_ID}...")
    try:
        deployments = agent_engines.list()
        return list(deployments)
    except Exception as e:
        print(f"Error listing deployments: {e}")
        return []

if __name__ == "__main__":
    deployments = list_deployments()
    
    if not deployments:
        print("No active deployments found.")
        sys.exit(0)

    print(f"Found {len(deployments)} deployment(s).")
    for app in deployments:
        print(f"- {app.resource_name} (Created: {app.create_time})")
        
    confirm = input("\nDo you want to delete ALL deployments listed above? (y/n): ")
    if confirm.lower() == 'y':
        for app in deployments:
            print(f"Deleting {app.resource_name}...")
            agent_engines.delete(app.resource_name)
        print("Done.")
    else:
        print("Cleanup cancelled.")
