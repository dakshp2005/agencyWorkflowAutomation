from datetime import datetime
from app.extensions import db

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    proposed_slots = db.Column(db.JSON)         # List of ISO datetime strings
    confirmed_slot = db.Column(db.String(50))
    calendar_event_id = db.Column(db.String(200))
    meeting_link = db.Column(db.String(300))
    agenda = db.Column(db.Text)
    status = db.Column(db.String(20), default='proposed')  # proposed | confirmed | cancelled | completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
