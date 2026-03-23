import os
from google.adk.agents import LlmAgent, SequentialAgent, LoopAgent
from google.adk.tools import google_search, AgentTool
from finance_advisor.tools import (
    calculate_monthly_budget, 
    convert_currency, 
    calculate_compound_interest
)
from finance_advisor.instructions import (
    CLASSIFIER_INSTRUCTION,
    ROUTER_INSTRUCTION,
    EXPENSE_ANALYZER_INSTRUCTION,
    BUDGET_ADVISOR_INSTRUCTION,
    GOAL_PROPOSER_INSTRUCTION,
    GOAL_EVALUATOR_INSTRUCTION,
    CURRENCY_CONVERTER_INSTRUCTION,
    FINANCE_TUTOR_INSTRUCTION,
    FORMATTER_INSTRUCTION
)
from finance_advisor.schemas import (
    QueryClassification,
    AdvisorResponse
)
from finance_advisor.callback import (
    before_model_safety_screen,
    before_tool_validate_args,
    after_agent_log_lifecycle
)

MODEL_NAME = os.environ.get("GOOGLE_GENAI_MODEL", "gemini-2.5-flash")

# --- Specialist 1: Expense Analyzer ---
expense_agent = LlmAgent(
    name="ExpenseAnalyzer",
    model=MODEL_NAME,
    instruction=EXPENSE_ANALYZER_INSTRUCTION,
    output_key="expense_findings",
    after_agent_callback=after_agent_log_lifecycle
)

# --- Specialist 2: Budget Advisor ---
budget_agent = LlmAgent(
    name="BudgetAdvisor",
    model=MODEL_NAME,
    instruction=BUDGET_ADVISOR_INSTRUCTION,
    tools=[calculate_monthly_budget],
    output_key="budget_findings",
    before_tool_callback=before_tool_validate_args,
    after_agent_callback=after_agent_log_lifecycle
)

# --- Specialist 3: Goal Tracker (Iterative Loop) ---
goal_proposer = LlmAgent(
    name="GoalProposer",
    model=MODEL_NAME,
    instruction=GOAL_PROPOSER_INSTRUCTION,
    tools=[calculate_compound_interest],
    output_key="goal_proposal",
    before_tool_callback=before_tool_validate_args
)

goal_evaluator = LlmAgent(
    name="GoalEvaluator",
    model=MODEL_NAME,
    instruction=GOAL_EVALUATOR_INSTRUCTION,
    output_key="goal_feedback"
)

# Terminate loop when state['goal_approved'] is True
goal_loop = LoopAgent(
    name="GoalTrackerLoop",
    sub_agents=[goal_proposer, goal_evaluator],
    max_iterations=3
)

# --- Specialist 4: Currency Converter ---
currency_agent = LlmAgent(
    name="CurrencyConverter",
    model=MODEL_NAME,
    instruction=CURRENCY_CONVERTER_INSTRUCTION,
    tools=[convert_currency],
    output_key="currency_findings",
    before_tool_callback=before_tool_validate_args,
    after_agent_callback=after_agent_log_lifecycle
)

# --- Specialist 5: Finance Tutor ---
education_agent = LlmAgent(
    name="FinanceTutor",
    model=MODEL_NAME,
    instruction=FINANCE_TUTOR_INSTRUCTION,
    tools=[google_search],
    output_key="education_findings",
    after_agent_callback=after_agent_log_lifecycle
)

# --- Orchestration Tier ---

# 1. Intent Classification (Attach Global Safety Screen here)
classifier_agent = LlmAgent(
    name="IntentClassifier",
    model=MODEL_NAME,
    instruction=CLASSIFIER_INSTRUCTION,
    output_schema=QueryClassification,
    output_key="query_classification",
    before_model_callback=before_model_safety_screen,
    after_agent_callback=after_agent_log_lifecycle
)

# 2. Router (Agent-as-a-Tool)
expense_tool = AgentTool(agent=expense_agent)
budget_tool = AgentTool(agent=budget_agent)
goal_tool = AgentTool(agent=goal_loop)
currency_tool = AgentTool(agent=currency_agent)
education_tool = AgentTool(agent=education_agent)

router_agent = LlmAgent(
    name="FinanceRouter",
    model=MODEL_NAME,
    instruction=ROUTER_INSTRUCTION,
    tools=[expense_tool, budget_tool, goal_tool, currency_tool, education_tool],
    output_key="router_summaries",
    after_agent_callback=after_agent_log_lifecycle
)

# 3. Final Formatter
formatter_agent = LlmAgent(
    name="ResponseFormatter",
    model=MODEL_NAME,
    instruction=FORMATTER_INSTRUCTION,
    output_schema=AdvisorResponse,
    output_key="final_advisor_response",
    after_agent_callback=after_agent_log_lifecycle
)

# --- ROOT AGENT PIPELINE ---
root_agent = SequentialAgent(
    name="FinanceAdvisor",
    sub_agents=[classifier_agent, router_agent, formatter_agent]
)
