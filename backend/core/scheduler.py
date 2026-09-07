from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

def fetch_latest_news():
    logger.info("[Scheduler] Fetching latest news for watchlisted startups...")
    # Trigger LangGraph workflows for news gathering here

def check_funding_alerts():
    logger.info("[Scheduler] Checking for recent funding rounds...")
    # Trigger LangGraph funding agent workflows

def generate_daily_reports():
    logger.info("[Scheduler] Generating daily executive reports...")
    # Trigger PDF generation logic

def setup_scheduler():
    # Every 5 min -> News
    scheduler.add_job(fetch_latest_news, IntervalTrigger(minutes=5), id="fetch_news", replace_existing=True)
    
    # Every 10 min -> Funding
    scheduler.add_job(check_funding_alerts, IntervalTrigger(minutes=10), id="check_funding", replace_existing=True)
    
    # Daily -> Executive report (Simulating daily with hours=24)
    scheduler.add_job(generate_daily_reports, IntervalTrigger(hours=24), id="generate_reports", replace_existing=True)
    
    scheduler.start()
    logger.info("APScheduler started successfully.")
