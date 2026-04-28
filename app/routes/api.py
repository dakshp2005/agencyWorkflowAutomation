from flask import Blueprint, request, jsonify
from urllib.parse import urlencode, quote
from app.services.email_service import email_service
from app.services.reply_classifier import reply_classifier
from app.services.scheduler_service import scheduler_service
from app.services.document_service import document_service
from app.services.rag_service import rag_service
from app.models.client import Client
from app.models.email_record import EmailRecord
from app.models.meeting import Meeting
from app.models.document import Document
from app.extensions import db

bp = Blueprint('api', __name__)

@bp.route('/clients', methods=['POST'])
def create_client():
    data = request.json
    c = Client(
        name=data.get('name'), email=data.get('email'), company=data.get('company'),
        industry=data.get('industry'), website=data.get('website'), phone=data.get('phone'),
        preferences=data.get('preferences'), notes=data.get('notes')
    )
    db.session.add(c)
    db.session.commit()
    text = f"Client: {c.name}, Company: {c.company}, Industry: {c.industry}, Preferences: {c.preferences}, Notes: {c.notes}"
    rag_service.add_document(text, c.id, "registration")
    return jsonify({"id": c.id}), 201

@bp.route('/outreach/generate', methods=['POST'])
def generate_email():
    data = request.json
    res = email_service.generate_outreach_email(data['client_id'], data.get('type', 'outreach'))
    return jsonify(res)

@bp.route('/outreach/send/<int:id>', methods=['POST'])
def send_email(id):
    try:
        email_service.send_email(id)
        return jsonify({"status": "sent"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/replies/fetch', methods=['POST'])
def fetch_replies():
    res = reply_classifier.fetch_and_classify()
    return jsonify({"processed": len(res), "items": res})

@bp.route('/meetings/propose', methods=['POST'])
def propose_meeting():
    client_id = request.json['client_id']
    mid = scheduler_service.propose_meeting(client_id)
    return jsonify({"meeting_id": mid})

@bp.route('/meetings/<int:id>/confirm', methods=['POST'])
def confirm_meeting(id):
    slot = request.json['chosen_slot']
    res = scheduler_service.confirm_meeting(id, slot)
    return jsonify(res)

@bp.route('/documents/generate', methods=['POST'])
def generate_document():
    data = request.json
    client_id = data['client_id']
    doc_type = data.get('doc_type', 'proposal')
    if doc_type == 'proposal':
        res = document_service.generate_proposal(client_id)
    else:
        res = document_service.generate_report(client_id)
    return jsonify(res)

@bp.route('/approve/email/<int:id>', methods=['POST', 'GET'])
def approve_email(id):
    record = EmailRecord.query.get_or_404(id)
    record.status = 'approved'
    db.session.commit()

    query = urlencode(
        {
            "subject": record.subject or "",
            "body": record.body or ""
        },
        quote_via=quote,
    )
    compose_url = f"mailto:{record.client.email}?{query}"
    return jsonify({"status": "approved", "compose_url": compose_url})

@bp.route('/reject/email/<int:id>', methods=['POST', 'GET'])
def reject_email(id):
    email_service.reject_email(id)
    return jsonify({"status": "rejected"})

@bp.route('/approve/proposal/<int:id>', methods=['POST', 'GET'])
def approve_proposal(id):
    doc = Document.query.get_or_404(id)
    doc.status = 'approved'
    db.session.commit()
    return jsonify({"status": "approved"})

@bp.route('/reject/proposal/<int:id>', methods=['POST', 'GET'])
def reject_proposal(id):
    doc = Document.query.get_or_404(id)
    doc.status = 'draft'
    db.session.commit()
    return jsonify({"status": "rejected"})

@bp.route('/approve/meeting/<int:id>', methods=['POST', 'GET'])
def approve_meeting(id):
    meeting = Meeting.query.get_or_404(id)
    # Pick first slot for quick approval
    slot = meeting.proposed_slots[0]
    res = scheduler_service.confirm_meeting(id, slot)
    return jsonify({"status": "confirmed", "slot": slot})

@bp.route('/rag/reindex', methods=['POST'])
def reindex_rag():
    rag_service.index_all_existing_data()
    return jsonify({"status": "indexed"})

@bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@bp.route('/stats', methods=['GET'])
def stats():
    pending_emails = EmailRecord.query.filter_by(status='pending_approval').count()
    pending_docs = Document.query.filter_by(status='pending_approval').count()
    return jsonify({"pending_approvals": pending_emails + pending_docs})
