from datetime import datetime
from app.extensions import db

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    title = db.Column(db.String(200))
    doc_type = db.Column(db.String(30))   # proposal | report | summary | followup
    content = db.Column(db.Text)
    file_path = db.Column(db.String(300))
    status = db.Column(db.String(20), default='draft')  # draft | pending_approval | approved | delivered
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
