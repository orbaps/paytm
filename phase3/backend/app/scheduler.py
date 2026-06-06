from apscheduler.schedulers.background import BackgroundScheduler
from app.db.database import SessionLocal
from app.services.engine import process_queue_worker, check_thresholds_worker

scheduler = BackgroundScheduler()

def threshold_job():
    db = SessionLocal()
    try:
        check_thresholds_worker(db)
    finally:
        db.close()

def queue_job():
    db = SessionLocal()
    try:
        process_queue_worker(db)
    finally:
        db.close()

def start_scheduler():
    scheduler.add_job(threshold_job, 'interval', seconds=10)
    scheduler.add_job(queue_job, 'interval', seconds=15)
    scheduler.start()
