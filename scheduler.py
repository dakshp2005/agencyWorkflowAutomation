from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import atexit

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    
    def fetch_replies_job():
        with app.app_context():
            try:
                from app.services.reply_classifier import reply_classifier
                reply_classifier.fetch_and_classify()
            except Exception as e:
                print(f"[Scheduler] Error in fetch_replies_job: {e}")
    
    def followup_check_job():
        """Check for clients who haven't replied in 3+ days and need followup"""
        with app.app_context():
            try:
                from app.models.client import Client
                from app.models.email_record import EmailRecord
                from app.services.email_service import email_service
                from datetime import datetime, timedelta
                cutoff = datetime.utcnow() - timedelta(days=3)
                stale = Client.query.filter_by(status='outreach_sent').filter(
                    Client.updated_at < cutoff
                ).all()
                for client in stale:
                    email_service.generate_outreach_email(client.id, email_type="followup")
            except Exception as e:
                print(f"[Scheduler] Error in followup_check_job: {e}")
    
    # Fetch and classify replies every 15 minutes
    scheduler.add_job(fetch_replies_job, IntervalTrigger(minutes=15), id='fetch_replies')
    
    # Check for follow-ups daily at 9am
    scheduler.add_job(followup_check_job, CronTrigger(hour=9, minute=0), id='followup_check')
    
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    return scheduler
