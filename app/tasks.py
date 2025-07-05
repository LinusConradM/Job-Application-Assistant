from apscheduler.schedulers.background import BackgroundScheduler

from .database import SessionLocal, init_db
from .models import Job
from .scraper import JobScraper
from .config import settings


def scrape_and_store():
    init_db()
    scraper = JobScraper()
    jobs = scraper.fetch_jobs()
    session = SessionLocal()
    for job_data in jobs:
        job = Job(**job_data)
        session.add(job)
    session.commit()
    session.close()
    scraper.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        scrape_and_store,
        "interval",
        minutes=settings.SCRAPE_INTERVAL_MINUTES,
        next_run_time=None,
    )
    scheduler.start()
    scrape_and_store()
    return scheduler