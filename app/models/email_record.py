from datetime import datetime
from app.extensions import db

class EmailRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    subject = db.Column(db.String(300))
    body = db.Column(db.Text)
    email_type = db.Column(db.String(30), default='outreach')  # outreach | followup | custom
    status = db.Column(db.String(20), default='draft')         # draft | pending_approval | approved | sent | failed
    approved_by = db.Column(db.String(80))
    sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
