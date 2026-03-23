# frontend/app.py
import streamlit as st
import os
import uuid
import json
import asyncio
from dotenv import load_dotenv
from google.genai import types

# Add parent directory to path to import finance_advisor
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

# --- Page Config ---
st.set_page_config(
    page_title="Finance Advisor AI",
    page_icon="🏦",
    layout="wide"
)

# Load CSS
with open(os.path.join(os.path.dirname(__file__), "style.css"), "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- State Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# --- Header ---
st.markdown("""
<div class='advisor-header'>
    <h1>🏦 AI Personal Finance Advisor</h1>
    <p style='color: #e2e8f0; font-size: 1.1rem;'>Professional Grade Financial Intelligence & Strategic Planning</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### ⚙️ Advisor Configuration")
    mode = st.radio("Execution Mode", ["Local (Dev)", "Vertex AI (Prod)"], disabled=not os.environ.get("PROJECT_ID"))
    
    st.divider()
    st.markdown("### 🛡️ Guardrail Status")
    st.markdown("<span class='status-badge'>PII Redaction: ACTIVE</span>", unsafe_allow_html=True)
    st.markdown("<span class='status-badge'>Safety Shield: ACTIVE</span>", unsafe_allow_html=True)
    
    st.divider()
    if st.button("Reset Session", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

# --- Local Agent Engine Setup ---
def get_local_agent():
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from finance_advisor.agent import root_agent
    
    session_service = InMemorySessionService()
    runner = Runner(agent=root_agent, session_service=session_service, app_name="FinanceAdvisor")
    return runner

# --- Chat Logic ---
async def process_query(query: str):
    runner = get_local_agent()
    session = runner.session_service.create_session(user_id="streamlit_user")
    
    # Simulate streaming (ADK Runner.run returns a generator)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # We wrap the generator as it might block or have internal async parts
        for event in runner.run(query=query, session_id=session.id):
            # Inspect event type and content
            # ADK events are typically dictionaries with 'type' and 'content'
            if event.get('type') == 'agent_response':
                full_response = event.get('content', {}).get('text', '')
                response_placeholder.markdown(full_response)
            elif event.get('type') == 'tool_call':
                st.info(f"🛠️ Agent is using tool: `{event.get('content', {}).get('name')}`")
    
    return full_response

# --- Interface ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tell me about your financial goals..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Run the agent (simplifying for local execution since PROJECT_ID isn't set yet)
    # Note: In a real app we'd handle the async runner properly
    # For now, we use a simple sync block for the demo
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from finance_advisor.agent import root_agent
    from google.genai import types
    
    session_service = InMemorySessionService()
    runner = Runner(agent=root_agent, session_service=session_service, app_name="FinanceAdvisor")
    
    # Handle session creation which might return a coroutine
    session_res = session_service.create_session(user_id="user_123", app_name="FinanceAdvisor")
    if asyncio.iscoroutine(session_res):
        import asyncio
        # We need to run it in the event loop since we're in a sync context
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        session = loop.run_until_complete(session_res)
    else:
        session = session_res

    session_id = getattr(session, "id", None) or (session.get("id") if isinstance(session, dict) else None)
    
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        final_text = ""
        
        # Using the same logic as our verify_agent.py
        for event in runner.run(new_message=types.Content(role="user", parts=[types.Part.from_text(text=prompt)]), session_id=session_id, user_id="user_123"):
            if event.type == 'agent_start':
                st.caption(f"🚀 {event.agent_name} starting...")
            elif event.type == 'tool_call':
                st.status(f"🛠️ Running tool: **{event.tool_name}**", state="running")
            elif event.type == 'agent_response':
                # The final response from SequentialAgent usually comes from the last sub-agent
                content = event.content
                # st.write(f"DEBUG: Agent {event.agent_name} responded with type {type(content)}")
                
                if isinstance(content, dict):
                    if 'final_advisor_response' in content:
                        resp = content['final_advisor_response']
                        # Handle potential Pydantic objects or dicts
                        summary = getattr(resp, 'summary', None) or resp.get('summary', '')
                        advice = getattr(resp, 'detailed_advice', None) or resp.get('detailed_advice', [])
                        items = getattr(resp, 'action_items', None) or resp.get('action_items', [])
                        disclaimer = getattr(resp, 'disclaimer', None) or resp.get('disclaimer', '')
                        
                        final_text = f"### {summary}\n\n"
                        final_text += "**Advice:**\n" + "\n".join([f"- {a}" for a in advice]) + "\n\n"
                        final_text += "**Action Items:**\n" + "\n".join([f"- {a}" for a in items]) + "\n\n"
                        final_text += f"*Disclaimer: {disclaimer}*"
                    elif event.agent_name == "ResponseFormatter":
                        # If the content is the model itself (unwrapped)
                        final_text = f"### {content.get('summary', '')}\n\n"
                        final_text += "**Advice:**\n" + "\n".join([f"- {a}" for a in content.get('detailed_advice', [])]) + "\n\n"
                        final_text += "**Action Items:**\n" + "\n".join([f"- {a}" for a in content.get('action_items', [])]) + "\n\n"
                        final_text += f"*Disclaimer: {content.get('disclaimer', '')}*"
                elif isinstance(content, str):
                    # For specialists or router that might return strings
                    if event.agent_name == "ResponseFormatter" or event.agent_name == "FinanceAdvisor":
                        final_text = content
                
                if final_text:
                    response_placeholder.markdown(final_text)
        
        if not final_text:
            final_text = "I processed your request, but there was no final text generated. Please check the specialist logs."
            response_placeholder.markdown(final_text)
            
    st.session_state.messages.append({"role": "assistant", "content": final_text})
