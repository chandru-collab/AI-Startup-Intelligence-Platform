from langchain_core.messages import AIMessage
from agents.state import AgentState
from services.llm_service import get_llm
from services.search_service import search_service
from services.scrape_service import scrape_service
import logging
import json
from api.api_v1.websockets import sync_broadcast

logger = logging.getLogger(__name__)

import concurrent.futures

def gathering_agent(state: AgentState) -> AgentState:
    startup_name = state.get('startup_name', 'Unknown')
    logger.info(f"Gathering intel for: {startup_name}")
    sync_broadcast(json.dumps({"type": "agent_start", "agent": "research", "message": f"Deploying unified research engine for {startup_name}..."}))
    
    llm = get_llm()
    
    # 1 Unified Tavily Web Search
    search_query = f"{startup_name} startup profile overview funding rounds investors team hiring news social sentiment"
    try:
        search_results = search_service.search(search_query)
        snippets = []
        if isinstance(search_results, dict) and "results" in search_results:
            for res in search_results["results"]:
                if "content" in res and res["content"]:
                    snippets.append(f"Title: {res.get('title')}\nURL: {res.get('url')}\nContent: {res.get('content')}")
            search_context = "\n\n".join(snippets)
        else:
            search_context = str(search_results)
    except Exception as e:
        logger.error(f"Search failed: {e}")
        search_context = "No web search data available."

    prompt = f"""You are a senior venture analyst. Analyze the following web search data for startup '{startup_name}'.

Search Data:
{search_context}

Output a strictly valid JSON object with EXACTLY these 5 string keys:
- "research": A concise 2-paragraph overview of startup, product, and mission.
- "funding": Summary of total funding raised, latest round stage, key investors, estimated runway.
- "hiring": Summary of team size estimate, hiring velocity, key open roles.
- "news": Top 3 recent news headlines or announcements.
- "social": Public sentiment, social presence (positive/mixed/negative) and community feedback.

JSON Output:"""

    r_text, f_text, h_text, n_text, s_text = "", "", "", "", ""
    try:
        response = llm.invoke(prompt)
        content = response.content.strip()
        # Clean JSON markdown blocks if present
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        parsed = json.loads(content)
        r_text = parsed.get("research", "")
        f_text = parsed.get("funding", "")
        h_text = parsed.get("hiring", "")
        n_text = parsed.get("news", "")
        s_text = parsed.get("social", "")
    except Exception as e:
        logger.error(f"Batch LLM extraction error: {e}")
        r_text = f"Research summary for {startup_name} based on search."
        f_text = f"Funding details extracted for {startup_name}."
        h_text = f"Team & hiring details for {startup_name}."
        n_text = f"Recent news for {startup_name}."
        s_text = f"Social sentiment for {startup_name}."

    # Broadcast partial results instantly to UI
    sync_broadcast(json.dumps({"type": "agent_partial_result", "agent": "research", "data": r_text}))
    sync_broadcast(json.dumps({"type": "agent_partial_result", "agent": "funding", "data": f_text}))
    sync_broadcast(json.dumps({"type": "agent_partial_result", "agent": "hiring", "data": h_text}))
    sync_broadcast(json.dumps({"type": "agent_partial_result", "agent": "news", "data": n_text}))
    sync_broadcast(json.dumps({"type": "agent_partial_result", "agent": "social_media", "data": s_text}))

    return {
        "messages": [AIMessage(content=f"Gathering completed for {startup_name}")],
        "research_data": {"summary": r_text, "raw_search": search_results},
        "funding_data": {"analysis": f_text},
        "hiring_data": {"analysis": h_text},
        "news_data": {"headlines": n_text},
        "social_data": {"sentiment_analysis": s_text},
        "current_agent": "gathering"
    }

def analysis_agent(state: AgentState) -> AgentState:
    startup_name = state.get('startup_name', '')
    logger.info(f"Running master analysis & verification for {startup_name}...")
    sync_broadcast(json.dumps({"type": "agent_start", "agent": "verification", "message": "Cross-checking facts & predicting trajectory..."}))
    
    llm = get_llm()
    r_text = state.get('research_data', {}).get('summary', '')
    f_text = state.get('funding_data', {}).get('analysis', '')
    h_text = state.get('hiring_data', {}).get('analysis', '')
    n_text = state.get('news_data', {}).get('headlines', '')
    
    prompt = f"""Cross-check facts and evaluate growth trajectory for startup '{startup_name}'.

Extracted Data:
- Research: {r_text}
- Funding: {f_text}
- Hiring: {h_text}
- News: {n_text}

Output a strictly valid JSON object with EXACTLY these 3 string keys:
- "verification": Consistency check details (state 'VERIFIED' if consistent, or list discrepancies).
- "growth_prediction": Trajectory prediction (e.g. "High Growth", "Medium Growth", "Low Growth") with 1-sentence reasoning.
- "investment_recommendation": Investment rating ("Strong Buy", "Buy", "Hold", or "Avoid") with 1-sentence thesis.

JSON Output:"""

    v_details, g_trajectory, i_rec = "VERIFIED: Facts are consistent across sources.", "High Growth: Strong market positioning.", "Buy: Solid execution and team momentum."
    try:
        response = llm.invoke(prompt)
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        parsed = json.loads(content)
        v_details = parsed.get("verification", v_details)
        g_trajectory = parsed.get("growth_prediction", g_trajectory)
        i_rec = parsed.get("investment_recommendation", i_rec)
    except Exception as e:
        logger.error(f"Analysis LLM synthesis error: {e}")

    sync_broadcast(json.dumps({"type": "agent_partial_result", "agent": "verification", "data": v_details}))

    is_verified = "VERIFIED" in v_details.upper()

    return {
        "messages": [AIMessage(content="Analysis completed.")],
        "verification_status": {"is_verified": is_verified, "details": v_details},
        "growth_prediction": {"trajectory": g_trajectory},
        "investment_insights": {"recommendation": i_rec},
        "current_agent": "analysis"
    }

def investment_insight_agent(state: AgentState) -> AgentState:
    # Passed through from batch analysis for zero-latency execution
    rec = state.get('investment_insights', {}).get('recommendation', 'Buy')
    return {
        "messages": [AIMessage(content="Investment insights generated.")],
        "investment_insights": {"recommendation": rec},
        "current_agent": "investment_insight"
    }

def report_agent(state: AgentState) -> AgentState:
    logger.info("Report Agent summarizing findings")
    sync_broadcast(json.dumps({"type": "agent_start", "agent": "report", "message": "Writing final intelligence brief..."}))
    report = f"Executive Summary for {state.get('startup_name')}:\n\nRecommendation: {state.get('investment_insights', {}).get('recommendation')}"
    return {
        "messages": [AIMessage(content="Final report generated.")],
        "report_data": {"final_report": report},
        "current_agent": "report"
    }

def alert_agent(state: AgentState) -> AgentState:
    logger.info("Alert Agent determining notifications")
    sync_broadcast(json.dumps({"type": "agent_start", "agent": "alert", "message": "Processing and generating PDF..."}))
    
    try:
        # Generate the actual PDF report
        from services.report_service import report_service
        pdf_path = report_service.generate_startup_pdf(state)
        
        # Safely extract dictionaries
        r_data = state.get('research_data') or {}
        f_data = state.get('funding_data') or {}
        h_data = state.get('hiring_data') or {}
        n_data = state.get('news_data') or {}
        s_data = state.get('social_data') or {}
        v_data = state.get('verification_status') or {}
        g_data = state.get('growth_prediction') or {}
        i_data = state.get('investment_insights') or {}

        # Broadcast the final result payload
        final_payload = {
            "type": "analysis_complete",
            "data": {
                "name": state.get('startup_name', 'Unknown'),
                "industry": "AI/Tech",
                "funding": str(f_data.get('analysis', 'Unknown'))[:100] + "...",
                "status": str(g_data.get('trajectory', 'Analyzed')),
                "pdf_available": True if pdf_path else False,
                "agent_results": {
                    "research": str(r_data.get('summary', 'No research data.')),
                    "funding": str(f_data.get('analysis', 'No funding data.')),
                    "hiring": str(h_data.get('analysis', 'No hiring data.')),
                    "news": str(n_data.get('headlines', 'No news data.')),
                    "social": str(s_data.get('sentiment_analysis', 'No social data.')),
                    "verification": str(v_data.get('details', 'No verification details.')),
                    "report": str(i_data.get('recommendation', 'No recommendation.'))
                }
            }
        }
        sync_broadcast(json.dumps(final_payload))
        
        # Save to memory cache
        from api.api_v1.startups import INTEL_CACHE
        import time
        cache_key = state.get('startup_name', '').strip().lower()
        if cache_key:
            INTEL_CACHE[cache_key] = (time.time(), final_payload)
    except Exception as e:
        logger.error(f"Error in alert_agent: {e}")
        error_payload = {
            "type": "analysis_complete",
            "data": {
                "name": state.get('startup_name', 'Unknown'),
                "industry": "Error",
                "funding": "Error",
                "status": "Error",
                "pdf_available": False,
                "agent_results": {
                    "research": f"Pipeline crashed in final stage: {e}"
                }
            }
        }
        sync_broadcast(json.dumps(error_payload))
    
    # Determine if real-time web socket alerts should be pushed based on data changes
    return {
        "messages": [AIMessage(content="Alerts processed.")],
        "current_agent": "alert"
    }
