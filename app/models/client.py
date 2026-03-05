from datetime import datetime
from app.extensions import db

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    company = db.Column(db.String(120))
    industry = db.Column(db.String(80))
    website = db.Column(db.String(200))
    phone = db.Column(db.String(30))
    preferences = db.Column(db.Text)           # Free text: tone, interests, requirements
    notes = db.Column(db.Text)                 # Internal notes
    status = db.Column(db.String(30), default='new')  
    # status options: new | outreach_sent | replied | meeting_scheduled | proposal_sent | converted | not_interested
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    emails = db.relationship('EmailRecord', backref='client', lazy=True)
    replies = db.relationship('InboundReply', backref='client', lazy=True)
    meetings = db.relationship('Meeting', backref='client', lazy=True)
    documents = db.relationship('Document', backref='client', lazy=True)
    logs = db.relationship('InteractionLog', backref='client', lazy=True)
