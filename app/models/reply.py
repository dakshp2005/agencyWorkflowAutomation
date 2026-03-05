from datetime import datetime
from app.extensions import db

class InboundReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
    sender_email = db.Column(db.String(120))
    subject = db.Column(db.String(300))
    raw_body = db.Column(db.Text)
    classification = db.Column(db.String(20))   # positive | negative | neutral
    extracted_entities = db.Column(db.JSON)     # {dates:[], companies:[], requirements:[]}
    action_taken = db.Column(db.String(100))
    processed_at = db.Column(db.DateTime, default=datetime.utcnow)
