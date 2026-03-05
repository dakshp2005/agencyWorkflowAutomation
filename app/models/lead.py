from app.extensions import db
from datetime import datetime

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    website = db.Column(db.String(200))
    email = db.Column(db.String(120))
    industry = db.Column(db.String(100))
    domain_topic = db.Column(db.String(100)) # e.g. "AI SaaS", "Healthcare"
    
    description = db.Column(db.Text)
    icp_score = db.Column(db.Integer, default=0) # 0-100
    icp_reasoning = db.Column(db.Text)
    
    status = db.Column(db.String(20), default='new') # new | qualified | converted | rejected
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Lead {self.company}>'
