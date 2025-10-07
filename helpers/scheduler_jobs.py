from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import logging
from helpers.wellness_client import WellnessClient
from helpers.sheets_client import SheetsClient
from config import SCHEDULED_WEEKLY_JOB_HOUR

logger = logging.getLogger(__name__)

def update_weekly_schedule():
    try:
        wc = WellnessClient()
        # Get next week range: next Monday -> Sunday
        today = datetime.utcnow().date()
        # find next week's Monday
        start = today + timedelta(days=(7 - today.weekday()))  # next Monday
        end = start + timedelta(days=6)
        start_str = start.isoformat()
        end_str = end.isoformat()
        classes = wc.get_schedule(start_str, end_str)
        # Optionally push to Google Sheets or internal store
        sc = SheetsClient()
        # Write a simple summary row for each class (or maintain a dedicated sheet)
        for c in classes:
            sc.sheet.append_row([
                f"Schedule: {c.get('title')}",
                "",
                "",
                c.get("location") or "",
                c.get("title") or "",
                c.get("startTime") or "",
                "",
                "ScheduleUpdate",
                "WellnessLiving",
                datetime.utcnow().isoformat()
            ])
        logger.info("Weekly schedule update completed")
    except Exception as e:
        logger.exception("Failed to update weekly schedule: %s", e)

def start_scheduler():
    sched = BackgroundScheduler(timezone="UTC")
    # Schedule every Sunday at configured hour (UTC)
    sched.add_job(update_weekly_schedule, "cron", day_of_week="sun", hour=SCHEDULED_WEEKLY_JOB_HOUR, minute=0)
    sched.start()
    return sched
