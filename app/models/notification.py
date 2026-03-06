from datetime import datetime
from app.extensions import db

class Notification(db.Model):
    """Track system notifications for approval requests and important events"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text)
    notification_type = db.Column(db.String(50))  # email_approval, document_approval, meeting_created, etc.
    related_id = db.Column(db.Integer)  # ID of the related entity (email, document, meeting, etc.)
    related_type = db.Column(db.String(50))  # 'email', 'document', 'meeting', etc.
    is_read = db.Column(db.Boolean, default=False)
    action_url = db.Column(db.String(300))  # URL to navigate to when clicked
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Notification {self.title}>'
