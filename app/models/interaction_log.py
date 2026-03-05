from datetime import datetime
from app.extensions import db

class InteractionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
    action_type = db.Column(db.String(50))  # email_generated | email_sent | reply_classified | 
                                             # meeting_proposed | meeting_confirmed | 
                                             # document_generated | approval_requested | approval_granted
    description = db.Column(db.Text)
    metadata_info = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
