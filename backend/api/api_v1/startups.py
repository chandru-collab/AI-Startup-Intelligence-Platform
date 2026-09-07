from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from agents.workflow import app_workflow
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ResearchRequest(BaseModel):
    startup_name: str

import time
import json
from api.api_v1.websockets import sync_broadcast

INTEL_CACHE = {}
CACHE_TTL = 3600  # 1 hour cache

def run_agent_pipeline_sync(startup_name: str):
    try:
        cache_key = startup_name.strip().lower()
        now = time.time()
        if cache_key in INTEL_CACHE:
            cached_time, cached_payload = INTEL_CACHE[cache_key]
            if now - cached_time < CACHE_TTL:
                logger.info(f"Serving cached intel for {startup_name}")
                agent_results = cached_payload.get("data", {}).get("agent_results", {})
                for agent_name, content in agent_results.items():
                    sync_broadcast(json.dumps({
                        "type": "agent_partial_result",
                        "agent": agent_name,
                        "data": content
                    }))
                sync_broadcast(json.dumps(cached_payload))
                return

        initial_state = {
            "startup_name": startup_name,
            "research_data": {},
            "funding_data": {},
            "hiring_data": {},
            "news_data": {},
            "social_data": {},
            "verification_status": {},
            "growth_prediction": {},
            "investment_insights": {},
            "report_data": {},
            "alert_status": ""
        }
        logger.info(f"Background pipeline started for {startup_name}")
        app_workflow.invoke(initial_state)
        logger.info(f"Background pipeline finished for {startup_name}")
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        logger.error(f"Error in background pipeline: {e}\n{tb}")
        from api.api_v1.websockets import sync_broadcast
        import json
        error_payload = {
            "type": "analysis_complete",
            "data": {
                "name": startup_name,
                "industry": "Error",
                "funding": "Error",
                "status": "Pipeline Failed",
                "pdf_available": False,
                "agent_results": {
                    "research": f"Global pipeline crash: {e}\nTraceback: {tb}"
                }
            }
        }
        sync_broadcast(json.dumps(error_payload))
@router.post("/research")
async def trigger_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    try:
        # Kick off the heavy 60-second LangGraph workflow in the background
        # so the frontend doesn't hang and time out!
        background_tasks.add_task(run_agent_pipeline_sync, request.startup_name)
        
        return {
            "status": "success",
            "message": f"AI Agents dispatched for {request.startup_name}. They are analyzing now in the background.",
            "data": {
                "name": request.startup_name,
                "industry": "Analyzing...",
                "funding": "Analyzing...",
                "status": "Agents Dispatched"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



from fastapi.responses import FileResponse
import os
import glob

@router.get("/{startup_name}/report/pdf")
async def download_startup_report(startup_name: str):
    reports_dir = "generated_reports"
    if not os.path.exists(reports_dir):
        raise HTTPException(status_code=404, detail="No reports generated yet.")
        
    # Find the most recent PDF for this startup
    search_pattern = os.path.join(reports_dir, f"{startup_name}_*.pdf")
    files = glob.glob(search_pattern)
    
    if not files:
        raise HTTPException(status_code=404, detail="PDF report not found for this startup.")
        
    latest_file = max(files, key=os.path.getctime)
    return FileResponse(latest_file, media_type='application/pdf', filename=f"{startup_name}_Intelligence_Report.pdf")
