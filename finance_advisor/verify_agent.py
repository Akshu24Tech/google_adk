# verify_agent.py
import os
import sys
import asyncio
from dotenv import load_dotenv
from google.genai import types

# Add current directory to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from finance_advisor import root_agent

def run_test(query_text, user_id, session_id, session_service):
    print(f"\n--- Testing Query: '{query_text}' ---")
    runner = Runner(agent=root_agent, session_service=session_service, app_name="FinanceAdvisor")
    
    # Wrap text in Content object
    user_message = types.Content(
        role="user",
        parts=[types.Part(text=query_text)]
    )
    
    try:
        print("Executing agent...")
        # Based on inspector, this is a synchronous generator
        for event in runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=user_message
        ):
            # Check for final response event
            if hasattr(event, "is_final_response") and event.is_final_response():
                print("\nFINAL ADVISOR RESPONSE:")
                content = event.content
                if content and hasattr(content, "parts"):
                    for part in content.parts:
                        if hasattr(part, "text"):
                            print(part.text)
            elif isinstance(event, dict) and event.get("type") == "final_response":
                 print(event.get("content"))
    except Exception as e:
        print(f"Error during run: {e}")

async def main():
    session_service = InMemorySessionService()
    user_id = "test_user_123"
    
    state_context = {
        "user_name": "Akshu",
        "monthly_income": 60000,
        "base_expenses": 30000,
        "currency": "INR",
        "financial_goals": ["Buy a car", "Retirement fund"]
    }
    
    # create_session - handle both
    res = session_service.create_session(
        app_name="FinanceAdvisor",
        user_id=user_id,
        state=state_context
    )
    if asyncio.iscoroutine(res):
        session = await res
    else:
        session = res
            
    session_id = getattr(session, "id", None) or session.get("id")
    print(f"Started session: {session_id}")
    
    # Run tests synchronously (generator)
    run_test("What is 500 USD in INR?", user_id, session_id, session_service)
    run_test("I spent 15000 on rent and 5000 on groceries last month. How is my budget?", user_id, session_id, session_service)

if __name__ == "__main__":
    print("Running tests...")
    asyncio.run(main())
