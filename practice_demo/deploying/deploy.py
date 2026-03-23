import os

from dotenv import load_dotenv

load_dotenv()

import vertexai
from social_posts_agent.agent import root_agent
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

PROJECT_ID = os.environ.get("PROJECT_ID", "YOUR_PROJECT_ID")
LOCATION = os.environ.get("LOCATION", "us-central1")
STAGING_BUCKET = os.environ.get("STAGING_BUCKET", "gs://YOUR_BUCKET_NAME")

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

remote_app = agent_engines.create(
    agent_engine=app,
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]",
        "litellm",
        "pydantic",
        "python-dotenv",
    ],
    env_vars=[
        "GOOGLE_API_KEY",
        "GOOGLE_GENAI_USE_VERTEXAI",
        "GOOGLE_GENAI_MODEL",
    ],
    extra_packages=["./social_posts_agent"],
)

print(f"Remote app created: {remote_app.resource_name}")