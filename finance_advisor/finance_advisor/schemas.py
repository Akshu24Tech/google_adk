from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict

class QueryCategory(str, Enum):
    EXPENSE_ANALYSIS = "expense_analysis"
    BUDGET_ADVICE = "budget_advice"
    GOAL_TRACKING = "goal_tracking"
    CURRENCY_CONVERSION = "currency_conversion"
    FINANCIAL_EDUCATION = "financial_education"

class QueryClassification(BaseModel):
    model_config = ConfigDict(extra='forbid')
    category: QueryCategory
    confidence: float = Field(ge=0.0, le=1.0)
    extracted_entities: Dict[str, str] = Field(default_factory=dict)

class ExpenseEntry(BaseModel):
    model_config = ConfigDict(extra='forbid')
    description: str
    amount: float
    category: str
    date: Optional[str] = None

class AdvisorResponse(BaseModel):
    model_config = ConfigDict(extra='forbid')
    category: QueryCategory
    summary: str
    detailed_advice: List[str]
    action_items: List[str]
    disclaimer: str = "This is AI-generated guidance. Consult a certified financial advisor."