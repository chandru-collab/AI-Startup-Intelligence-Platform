from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    Core state for the LangGraph orchestrator.
    This state flows through all agents in the graph.
    """
    startup_name: str
    
    # Message history
    messages: Annotated[Sequence[BaseMessage], operator.add]
    
    # Extracted data dictionaries updated by respective agents
    research_data: dict
    funding_data: dict
    hiring_data: dict
    news_data: dict
    social_data: dict
    
    # Analysis & Predictions
    growth_prediction: dict
    investment_insights: dict
    report_data: dict
    verification_status: dict
    
    # Status flags
    is_verified: bool
    current_agent: str
    errors: list[str]
