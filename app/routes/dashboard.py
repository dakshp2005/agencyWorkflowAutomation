from flask import Blueprint, render_template
from app.models.email_record import EmailRecord
from app.models.reply import InboundReply
from app.models.meeting import Meeting
from app.models.document import Document
from app.models.interaction_log import InteractionLog
from app.models.client import Client
from datetime import datetime, timedelta

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    today = datetime.utcnow().date()
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    # Simple stats
    emails_sent = EmailRecord.query.filter_by(status='sent').filter(EmailRecord.sent_at >= today).count()
    replies_count = InboundReply.query.filter(InboundReply.processed_at >= today).count()
    meetings_week = Meeting.query.filter(Meeting.created_at >= week_ago).count()
    docs_gen = Document.query.count()
    
    recent_activity = InteractionLog.query.order_by(InteractionLog.timestamp.desc()).limit(15).all()
    
    pending_emails = EmailRecord.query.filter_by(status='pending_approval').all()
    pending_docs = Document.query.filter_by(status='pending_approval').all()
    
    # Client pipeline counts
    pipeline = {
        'new': Client.query.filter_by(status='new').count(),
        'outreach_sent': Client.query.filter_by(status='outreach_sent').count(),
        'replied': Client.query.filter_by(status='replied').count(),
        'meeting_scheduled': Client.query.filter_by(status='meeting_scheduled').count(),
        'proposal_sent': Client.query.filter_by(status='proposal_sent').count(),
        'converted': Client.query.filter_by(status='converted').count(),
    }
    
    return render_template('dashboard/index.html',
                           stats={
                               "emails": emails_sent,
                               "replies": replies_count,
                               "meetings": meetings_week,
                               "docs": docs_gen
                           },
                           recent_activity=recent_activity,
                           pending_emails=pending_emails,
                           pending_docs=pending_docs,
                           pipeline=pipeline)
