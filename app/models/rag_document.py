from datetime import datetime
from app.extensions import db

class RAGDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
    source_type = db.Column(db.String(30))   # email | reply | meeting_note | proposal | registration
    raw_text = db.Column(db.Text)
    chunk_count = db.Column(db.Integer, default=0)
    faiss_ids = db.Column(db.JSON)           # List of FAISS vector IDs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
