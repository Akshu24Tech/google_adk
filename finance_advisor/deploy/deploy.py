# deploy/deploy.py
import os
import sys
from dotenv import load_dotenv

# Add project root to path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

import vertexai
from finance_advisor.agent import root_agent
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

# These should be set in your .env file
PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("LOCATION", "us-central1")
STAGING_BUCKET = os.environ.get("STAGING_BUCKET")

if not PROJECT_ID or not STAGING_BUCKET:
    print("❌ ERROR: PROJECT_ID and STAGING_BUCKET must be set in your .env file for deployment.")
    exit(1)

print(f"🚀 Initializing Vertex AI in {PROJECT_ID} ({LOCATION})...")

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

# Initialize the ADK App wrapper
app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

print("📦 Creating Remote Agent Engine (this may take a few minutes)...")

# Deploy to Vertex AI
remote_app = agent_engines.create(
    agent_engine=app,
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]",
        "google-generativeai",
        "python-dotenv",
        "litellm",
        "pydantic",
        "requests",
    ],
    env_vars=[
        "GOOGLE_API_KEY",
        "GOOGLE_GENAI_USE_VERTEXAI",
        "GOOGLE_GENAI_MODEL",
    ],
    # Include the local package
    extra_packages=["./finance_advisor"],
)

print(f"✅ Remote app successfully created!")
print(f"Resource Name: {remote_app.resource_name}")
print("\nUpdate your .env or frontend config with this RESOURCE_ID to use it in production.")
