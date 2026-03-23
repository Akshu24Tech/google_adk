# 🚀 New Google ADK Concepts — Updated Finance Advisor Project

Your original project suggestion covers the **core ADK foundation** excellently. Since then, Google ADK has evolved significantly with powerful new capabilities. Here's what's new and how each concept fits into your **AI Personal Finance Advisor** project.

---

## 📊 What You Already Cover vs. What's New

| Status | Concept | Where in Project |
|--------|---------|-----------------|
| ✅ Already | `LlmAgent`, `SequentialAgent`, `ParallelAgent` | Root orchestrator, specialist agents |
| ✅ Already | Custom tools, `google_search` | Budget calc, currency API, tutor |
| ✅ Already | `output_schema`, `input_schema`, Pydantic | QueryClassification, AdvisorResponse |
| ✅ Already | `InMemorySessionService`, `Runner` | Session management |
| ✅ Already | All 6 callback types | Logging, PII redaction, validation |
| ✅ Already | `output_key`, state passing | Inter-agent communication |
| ✅ Already | Multi-model (`LiteLlm`) | Budget uses GPT, Classifier uses Gemini |
| ✅ Already | Vertex AI deployment | `AdkApp`, `agent_engines.create()` |
| ✅ Already | Streamlit frontend | Finance-themed chat UI |
| 🆕 **New** | **`LoopAgent`** | Iterative budget refinement |
| 🆕 **New** | **`AgentTool` (Agent-as-a-Tool)** | Wrap specialists as callable tools |
| 🆕 **New** | **A2A Protocol** | Cross-service agent communication |
| 🆕 **New** | **Bidirectional Streaming** | Voice-based finance assistant |
| 🆕 **New** | **MCP Tool Integration** | Connect to external data tools |
| 🆕 **New** | **Guardrails (Advanced)** | Input/output screening, sandboxing |
| 🆕 **New** | **Evaluation & Tracing** | Agent quality testing |
| 🆕 **New** | **Cloud Run Deployment** | Alternative to Vertex AI |

---

## 🆕 New Concepts Deep Dive

### 1. 🔄 `LoopAgent` — Iterative Budget Refinement

**What it is:** A workflow agent that repeats its sub-agents in a loop until a condition is met or max iterations reached. Operates deterministically (not LLM-powered itself).

**How to add to your project:**

Create a `BudgetRefinementLoop` that iteratively adjusts the user's budget based on their constraints:

```python
from google.adk.agents import LoopAgent, LlmAgent

# Sub-agent 1: Generate a budget proposal
budget_proposer = LlmAgent(
    name="BudgetProposer",
    model="gemini-2.5-flash",
    instruction="""Based on the user's income and goals in session state,
    propose a monthly budget allocation. Store as 'budget_proposal'.""",
    output_key="budget_proposal",
)

# Sub-agent 2: Evaluate if budget meets goals
budget_evaluator = LlmAgent(
    name="BudgetEvaluator",
    model="gemini-2.5-flash",
    instruction="""Review the budget_proposal and check if it meets
    the user's financial goals. If satisfied, set 
    state['budget_approved'] = True to stop the loop.
    Otherwise, provide feedback for refinement.""",
    output_key="budget_feedback",
)

# LoopAgent: iterate until budget is approved or max 5 tries
budget_loop = LoopAgent(
    name="BudgetRefinementLoop",
    sub_agents=[budget_proposer, budget_evaluator],
    max_iterations=5,
)
```

**Use cases in finance:** 
- Iteratively refine investment portfolio allocation
- Progressively optimize debt repayment plans
- Goal-seeking: adjust savings rate until a target is met

---

### 2. 🧰 `AgentTool` (Agent-as-a-Tool Pattern)

**What it is:** Wrap an entire agent as a tool using `AgentTool`. The parent agent stays in control and invokes specialist agents like function calls.

**How to add to your project:**

Instead of sub-agent delegation, the Router can use specialists as tools:

```python
from google.adk.tools import AgentTool

# Wrap specialist agents as tools
expense_tool = AgentTool(agent=expense_agent)
budget_tool = AgentTool(agent=budget_agent)
currency_tool = AgentTool(agent=currency_agent)
education_tool = AgentTool(agent=education_agent)

# Router agent uses them as tools (stays in control)
router_agent = LlmAgent(
    name="FinanceRouter",
    model="gemini-2.5-flash",
    instruction="""You are a finance advisor router. Based on the user's
    query, use the appropriate specialist tool. You maintain full control
    of the conversation and can combine results from multiple tools.""",
    tools=[expense_tool, budget_tool, currency_tool, education_tool],
)
```

**Why this matters:** The Router maintains orchestration control, can combine results from multiple specialists, and handles errors gracefully — unlike sub-agent delegation where control passes entirely.

---

### 3. 🌐 A2A Protocol (Agent-to-Agent Communication)

**What it is:** An open standard for agents to discover each other, exchange tasks, and collaborate across different services/frameworks. Uses Agent Cards (`.well-known/agent-card.json`) for discovery.

**How to add to your project:**

Expose your Finance Advisor as an A2A server that other agents can discover and call:

```python
# Expose as A2A server
from google.adk.agents import RemoteA2aAgent

# Your finance agent becomes discoverable via Agent Card
# Other apps/agents can send it queries like:
# "What's my budget status?" or "Convert 100 USD to INR"

# Or consume an external tax advisor agent:
tax_agent = RemoteA2aAgent(
    name="TaxAdvisor",
    agent_card_url="https://tax-service.example.com/.well-known/agent-card.json",
    description="External tax planning agent",
)
```

**Real-world use:** Your finance advisor could communicate with a separate tax agent, investment agent, or banking agent — each built by different teams or even different frameworks.

---

### 4. 🎙️ Bidirectional Streaming (Voice Finance Assistant)

**What it is:** Real-time two-way audio/video communication with agents using WebSockets and the Gemini Live API. Supports natural conversation with interruption handling.

**How to add to your project — Phase 9 Enhancement:**

```python
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

# Use run_live() for streaming
runner = Runner(
    agent=root_agent, 
    session_service=session_service,
    app_name="FinanceAdvisor"
)

# Start live streaming session
live_events = runner.run_live(
    session=session,
    live_request_queue=request_queue,  # LiveRequestQueue
)

# Build a FastAPI + WebSocket frontend for voice interaction
```

**Use case:** Ask your finance advisor questions by voice: *"Hey, how much did I spend on food this month?"* — and get spoken responses in real-time.

---

### 5. 🔌 MCP Tool Integration

**What it is:** Model Context Protocol connects agents to external tools and data sources via standardized servers. ADK supports MCP tools natively.

**How to add to your project:**

```python
from google.adk.tools.mcp_tool import MCPTool

# Connect to an MCP server for database access
db_tool = MCPTool(
    server_name="finance_db",
    tool_name="query_expenses",
)

# Use in your expense analyzer agent
expense_agent = LlmAgent(
    name="ExpenseAnalyzer",
    tools=[db_tool],
    instruction="Use the database tool to query expense records...",
)
```

**Use case:** Connect to a PostgreSQL MCP server, Google Sheets MCP server, or any other data source without writing custom API integration code.

---

### 6. 🛡️ Advanced Guardrails

**What it is:** Beyond your existing callbacks, ADK now provides a multi-layered security framework.

**New guardrail capabilities to add:**

```python
# 1. Use Gemini Flash Lite as a safety screener
def before_model_screen_content(callback_context, llm_request):
    """Use a fast, cheap model to screen inputs for safety."""
    import google.generativeai as genai
    screener = genai.GenerativeModel("gemini-2.0-flash-lite")
    result = screener.generate_content(
        f"Is this a safe financial query? Reply SAFE or UNSAFE: "
        f"{llm_request.contents[-1].parts[0].text}"
    )
    if "UNSAFE" in result.text:
        # Block the request
        return {"blocked": True, "reason": "Content policy violation"}

# 2. In-tool guardrails - limit database queries
def query_expenses(query: str, tool_context) -> dict:
    """Query expenses with built-in guardrails."""
    ALLOWED_TABLES = ["expenses", "budgets", "goals"]
    # Validate query only touches allowed tables
    if not any(table in query.lower() for table in ALLOWED_TABLES):
        return {"error": "Access denied: unauthorized table"}
    # ... execute query

# 3. Sandboxed code execution for financial calculations
from google.adk.tools import code_execution
calculator_agent = LlmAgent(
    name="FinanceCalculator",
    tools=[code_execution],  # Runs in sandbox
    instruction="Write Python code to calculate financial projections...",
)
```

---

### 7. 📊 Evaluation & Tracing

**What it is:** Built-in tools for evaluating agent quality, relevance, and correctness. Traces every decision for debugging.

**How to add to your project:**

```python
# Enable tracing in deployment
app = reasoning_engines.AdkApp(
    agent=root_agent, 
    enable_tracing=True  # ← Already in your deploy script!
)

# Write evaluation test cases
test_cases = [
    {
        "input": "Convert 100 USD to INR",
        "expected_agent": "CurrencyConverter",
        "expected_fields": ["converted", "rate"],
    },
    {
        "input": "I earn 50000, spent 30000. How am I doing?",
        "expected_agent": "BudgetAdvisor",
        "expected_fields": ["savings_rate"],
    },
]
```

**Use case:** Build a test suite that validates your agents route queries correctly and return expected structured outputs.

---

## 📋 Updated Architecture

```
User Query (Text / Voice 🆕)
    │
    ▼
┌───────────────────────────────────────────────────────────┐
│            FinanceAdvisorAgent (root)                      │
│              SequentialAgent                                │
│                                                            │
│  ┌────────────────────────────────────────────────────┐    │
│  │  1. Guardrail Screener (before_model callback) 🆕  │    │
│  │     - PII redaction + safety screening              │    │
│  └────────────────────────────────────────────────────┘    │
│                     │                                       │
│  ┌────────────────────────────────────────────────────┐    │
│  │  2. QueryClassifier (LlmAgent)                     │    │
│  │     - output_schema: QueryClassification             │    │
│  └────────────────────────────────────────────────────┘    │
│                     │                                       │
│  ┌────────────────────────────────────────────────────┐    │
│  │  3. FinanceRouter (LlmAgent) 🆕 USES AgentTool     │    │
│  │     tools=[expense_tool, budget_tool, goal_tool,    │    │
│  │            currency_tool, education_tool,            │    │
│  │            tax_agent_tool (remote A2A)] 🆕          │    │
│  └────────────────────────────────────────────────────┘    │
│       │        │         │         │        │       │      │
│       ▼        ▼         ▼         ▼        ▼       ▼      │
│  ┌───────┐┌───────┐┌────────┐┌───────┐┌──────┐┌──────┐   │
│  │Expense││Budget ││  Goal  ││Currenc││Financ││ Tax  │   │
│  │Analyz.││Advisor││Tracker ││y Conv.││Tutor ││A2A🆕│   │
│  ├───────┤├───────┤│(Loop🆕)│├───────┤├──────┤├──────┤   │
│  │MCP DB ││       │├────────┤│       ││Search││Remote│   │
│  │tool🆕││       ││Proposer││       ││      ││Agent │   │
│  └───────┘│       ││Evaluatr││       ││      ││      │   │
│           └───────┘└────────┘└───────┘└──────┘└──────┘   │
│                     │                                       │
│  ┌────────────────────────────────────────────────────┐    │
│  │  4. ResponseFormatter (LlmAgent)                    │    │
│  │     - output_schema: AdvisorResponse                │    │
│  └────────────────────────────────────────────────────┘    │
│                                                            │
│  Evaluation & Tracing enabled 🆕                           │
└───────────────────────────────────────────────────────────┘
          │
          ▼
    Frontend Options:
    ├── Streamlit Chat UI (existing)
    ├── Voice Assistant (WebSocket + Streaming) 🆕
    └── A2A Server (discoverable by other agents) 🆕
```

---

## 📋 Updated Phase Guide

Your original 10 phases remain the same. Here are **3 new phases** to add:

### **Phase 5.5: Add LoopAgent for Goal Tracking** (45 min, ⭐⭐⭐)
- Wrap the GoalTracker agent in a `LoopAgent` with `budget_proposer` + `budget_evaluator`
- Set `max_iterations=5` with a termination condition

### **Phase 5.6: Wrap Specialists with AgentTool** (30 min, ⭐⭐)
- Use `AgentTool` to wrap each specialist agent
- Update the Router to use tools[] instead of sub_agent delegation
- This gives the Router more control over the conversation

### **Phase 11: Add Voice Streaming** (2 hours, ⭐⭐⭐⭐)
- Build a FastAPI backend with WebSocket endpoints
- Use `Runner.run_live()` for bidirectional audio streaming
- Create a simple web client with microphone input

---

## 📈 Updated Timeline

| Phase | Time | Difficulty | New? |
|-------|------|-----------|------|
| 1. Setup | 30 min | ⭐ | |
| 2. Schemas | 30 min | ⭐⭐ | |
| 3. Tools | 1 hour | ⭐⭐ | |
| 4. Callbacks + Guardrails | 1.5 hours | ⭐⭐⭐ | 🆕 Enhanced |
| 5. Agent Pipeline | 1.5 hours | ⭐⭐⭐⭐ | |
| 5.5 LoopAgent | 45 min | ⭐⭐⭐ | 🆕 |
| 5.6 AgentTool Pattern | 30 min | ⭐⭐ | 🆕 |
| 6. Sessions | 30 min | ⭐⭐ | |
| 7. Local Testing + Evaluation | 1 hour | ⭐⭐⭐ | 🆕 Enhanced |
| 8. Deploy | 1 hour | ⭐⭐⭐ | |
| 9. Frontend | 2 hours | ⭐⭐⭐ | |
| 10. Cleanup | 15 min | ⭐ | |
| 11. Voice Streaming | 2 hours | ⭐⭐⭐⭐ | 🆕 |
| **Total** | **~12-13 hours** | | |

---

## 🎯 Summary of New Concepts You'll Learn

| # | New Concept | ADK Feature | Difficulty |
|---|------------|-------------|-----------|
| 1 | Iterative refinement loops | `LoopAgent` | ⭐⭐⭐ |
| 2 | Agent-as-a-Tool pattern | `AgentTool` | ⭐⭐ |
| 3 | Cross-service agent communication | A2A Protocol, `RemoteA2aAgent` | ⭐⭐⭐⭐ |
| 4 | Real-time voice interaction | Bidirectional Streaming, `run_live()` | ⭐⭐⭐⭐ |
| 5 | External tool integration | MCP Tools | ⭐⭐⭐ |
| 6 | Multi-layer security | Advanced Guardrails, sandboxed execution | ⭐⭐⭐ |
| 7 | Quality assurance | Evaluation & Tracing | ⭐⭐ |

> **After completing the enhanced project, you'll have mastered:** Everything in the original plan **PLUS** `LoopAgent`, `AgentTool`, A2A protocol, bidirectional streaming, MCP integration, advanced guardrails, and evaluation — **the complete modern Google ADK stack**.
