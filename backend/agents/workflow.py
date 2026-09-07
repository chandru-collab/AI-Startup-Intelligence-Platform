from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.nodes import (
    gathering_agent, analysis_agent,
    investment_insight_agent,
    report_agent, alert_agent
)

def build_workflow():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("gathering", gathering_agent)
    workflow.add_node("analysis", analysis_agent)
    workflow.add_node("investment_insight", investment_insight_agent)
    workflow.add_node("report", report_agent)
    workflow.add_node("alert", alert_agent)
    
    # Define edges (Linear workflow using ThreadPools for parallelism)
    workflow.set_entry_point("gathering")
    workflow.add_edge("gathering", "analysis")
    workflow.add_edge("analysis", "investment_insight")
    workflow.add_edge("investment_insight", "report")
    workflow.add_edge("report", "alert")
    workflow.add_edge("alert", END)
    
    return workflow.compile()

app_workflow = build_workflow()
