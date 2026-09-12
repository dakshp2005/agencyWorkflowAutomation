from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from app.models.user import User
from app.models.client import Client
from app.models.email_record import EmailRecord
from app.models.meeting import Meeting
from app.models.document import Document
from app.models.lead import Lead
from app.models.interaction_log import InteractionLog
from app.models.notification import Notification
from app.extensions import db
from datetime import datetime
import os

spa = Blueprint('spa', __name__)


def spa_require_auth(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'spa_user_id' not in session:
            return jsonify({"error": "Not authenticated"}), 401
        return f(*args, **kwargs)
    return decorated


@spa.route('/login-page')
def login_page():
    return render_template('spa/login.html')


@spa.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"error": "Invalid email or password"}), 401

    if not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    session['spa_user_id'] = user.id
    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 200


@spa.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    company_name = data.get('company_name', '').strip()
    company_email = data.get('company_email', '').strip()
    password = data.get('password', '')
    company_type = data.get('company_type', '')
    company_description = data.get('company_description', '')
    user_role = data.get('user_role', '')

    if not company_name or not company_email or not password:
        return jsonify({"error": "Company name, email, and password are required"}), 400

    if User.query.filter_by(email=company_email).first():
        return jsonify({"error": "Email already registered"}), 400

    username = company_name.lower().replace(' ', '_').replace('.', '')
    base_username = username
    counter = 1
    while User.query.filter_by(username=username).first():
        username = f"{base_username}_{counter}"
        counter += 1

    new_user = User(username=username, email=company_email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    client = Client(
        name=company_name,
        email=company_email,
        company=company_name,
        industry=company_type,
        preferences=company_description,
        notes=f"Role: {user_role}" if user_role else None,
        status='new'
    )
    db.session.add(client)
    db.session.commit()

    return jsonify({
        "message": "Account created successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    }), 201


@spa.route('/logout', methods=['POST'])
def logout():
    session.pop('spa_user_id', None)
    return jsonify({"message": "Logged out"}), 200


@spa.route('/dashboard')
@spa_require_auth
def dashboard():
    user = db.session.get(User, session['spa_user_id'])
    if not user:
        session.pop('spa_user_id', None)
        return redirect('/login-page')

    clients = Client.query.order_by(Client.created_at.desc()).all()
    emails = EmailRecord.query.order_by(EmailRecord.created_at.desc()).limit(10).all()
    meetings = Meeting.query.order_by(Meeting.created_at.desc()).limit(10).all()
    documents = Document.query.order_by(Document.created_at.desc()).limit(10).all()
    leads = Lead.query.order_by(Lead.created_at.desc()).limit(10).all()
    notifications = Notification.query.filter_by(is_read=False).order_by(Notification.created_at.desc()).limit(10).all()
    recent_activity = InteractionLog.query.order_by(InteractionLog.timestamp.desc()).limit(15).all()

    pipeline = {
        'new': Client.query.filter_by(status='new').count(),
        'outreach_sent': Client.query.filter_by(status='outreach_sent').count(),
        'replied': Client.query.filter_by(status='replied').count(),
        'meeting_scheduled': Client.query.filter_by(status='meeting_scheduled').count(),
        'proposal_sent': Client.query.filter_by(status='proposal_sent').count(),
        'converted': Client.query.filter_by(status='converted').count(),
    }

    return render_template('spa/dashboard.html',
                           user=user,
                           clients=clients,
                           emails=emails,
                           meetings=meetings,
                           documents=documents,
                           leads=leads,
                           notifications=notifications,
                           recent_activity=recent_activity,
                           pipeline=pipeline)


@spa.route('/api/dashboard/stats')
@spa_require_auth
def dashboard_stats():
    today = datetime.utcnow().date()
    week_ago = datetime.utcnow() - __import__('datetime').timedelta(days=7)

    return jsonify({
        "stats": {
            "total_clients": Client.query.count(),
            "emails_sent": EmailRecord.query.filter_by(status='sent').filter(EmailRecord.sent_at >= today).count(),
            "replies_count": 0,
            "meetings_week": Meeting.query.filter(Meeting.created_at >= week_ago).count(),
            "docs_gen": Document.query.count(),
            "leads": Lead.query.count(),
        },
        "pipeline": {
            'new': Client.query.filter_by(status='new').count(),
            'outreach_sent': Client.query.filter_by(status='outreach_sent').count(),
            'replied': Client.query.filter_by(status='replied').count(),
            'meeting_scheduled': Client.query.filter_by(status='meeting_scheduled').count(),
            'proposal_sent': Client.query.filter_by(status='proposal_sent').count(),
            'converted': Client.query.filter_by(status='converted').count(),
        }
    })


@spa.route('/api/clients', methods=['GET'])
@spa_require_auth
def get_clients():
    clients = Client.query.order_by(Client.created_at.desc()).all()
    return jsonify([{
        "id": c.id, "name": c.name, "email": c.email,
        "company": c.company, "industry": c.industry,
        "website": c.website, "phone": c.phone,
        "preferences": c.preferences, "notes": c.notes,
        "status": c.status,
        "created_at": c.created_at.isoformat() if c.created_at else None,
        "updated_at": c.updated_at.isoformat() if c.updated_at else None,
    } for c in clients])


@spa.route('/api/clients', methods=['POST'])
@spa_require_auth
def create_client():
    data = request.get_json()
    c = Client(
        name=data.get('name'), email=data.get('email'), company=data.get('company'),
        industry=data.get('industry'), website=data.get('website'), phone=data.get('phone'),
        preferences=data.get('preferences'), notes=data.get('notes')
    )
    db.session.add(c)
    db.session.commit()
    return jsonify({"id": c.id, "message": "Client created"}), 201


@spa.route('/api/clients/<int:id>', methods=['GET'])
@spa_require_auth
def get_client(id):
    c = Client.query.get_or_404(id)
    return jsonify({
        "id": c.id, "name": c.name, "email": c.email,
        "company": c.company, "industry": c.industry,
        "website": c.website, "phone": c.phone,
        "preferences": c.preferences, "notes": c.notes,
        "status": c.status,
        "created_at": c.created_at.isoformat() if c.created_at else None,
    })


@spa.route('/api/clients/<int:id>', methods=['PUT'])
@spa_require_auth
def update_client(id):
    c = Client.query.get_or_404(id)
    data = request.get_json()
    for field in ['name', 'email', 'company', 'industry', 'website', 'phone', 'preferences', 'notes', 'status']:
        if field in data:
            setattr(c, field, data[field])
    db.session.commit()
    return jsonify({"message": "Client updated"})


@spa.route('/api/clients/<int:id>', methods=['DELETE'])
@spa_require_auth
def delete_client(id):
    c = Client.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({"message": "Client deleted"})


@spa.route('/api/emails', methods=['GET'])
@spa_require_auth
def get_emails():
    emails = EmailRecord.query.order_by(EmailRecord.created_at.desc()).all()
    return jsonify([{
        "id": e.id, "client_id": e.client_id,
        "subject": e.subject, "body": e.body,
        "email_type": e.email_type, "status": e.status,
        "sent_at": e.sent_at.isoformat() if e.sent_at else None,
        "created_at": e.created_at.isoformat() if e.created_at else None,
    } for e in emails])


@spa.route('/api/meetings', methods=['GET'])
@spa_require_auth
def get_meetings():
    meetings = Meeting.query.order_by(Meeting.created_at.desc()).all()
    return jsonify([{
        "id": m.id, "client_id": m.client_id,
        "proposed_slots": m.proposed_slots,
        "confirmed_slot": m.confirmed_slot,
        "meeting_link": m.meeting_link,
        "agenda": m.agenda, "status": m.status,
        "created_at": m.created_at.isoformat() if m.created_at else None,
    } for m in meetings])


@spa.route('/api/documents', methods=['GET'])
@spa_require_auth
def get_documents():
    docs = Document.query.order_by(Document.created_at.desc()).all()
    return jsonify([{
        "id": d.id, "client_id": d.client_id,
        "title": d.title, "doc_type": d.doc_type,
        "content": d.content, "status": d.status,
        "created_at": d.created_at.isoformat() if d.created_at else None,
    } for d in docs])


@spa.route('/api/leads', methods=['GET'])
@spa_require_auth
def get_leads():
    leads = Lead.query.order_by(Lead.created_at.desc()).all()
    return jsonify([{
        "id": l.id, "name": l.name, "company": l.company,
        "website": l.website, "email": l.email,
        "industry": l.industry, "domain_topic": l.domain_topic,
        "description": l.description,
        "icp_score": l.icp_score, "icp_reasoning": l.icp_reasoning,
        "status": l.status,
        "created_at": l.created_at.isoformat() if l.created_at else None,
    } for l in leads])


@spa.route('/api/activity', methods=['GET'])
@spa_require_auth
def get_activity():
    logs = InteractionLog.query.order_by(InteractionLog.timestamp.desc()).limit(20).all()
    return jsonify([{
        "id": l.id, "client_id": l.client_id,
        "action_type": l.action_type,
        "description": l.description,
        "timestamp": l.timestamp.isoformat() if l.timestamp else None,
    } for l in logs])


@spa.route('/api/notifications', methods=['GET'])
@spa_require_auth
def get_notifications():
    notifs = Notification.query.order_by(Notification.created_at.desc()).limit(20).all()
    return jsonify([{
        "id": n.id, "title": n.title,
        "message": n.message,
        "notification_type": n.notification_type,
        "is_read": n.is_read,
        "created_at": n.created_at.isoformat() if n.created_at else None,
    } for n in notifs])


@spa.route('/api/notifications/count', methods=['GET'])
@spa_require_auth
def notification_count():
    count = Notification.query.filter_by(is_read=False).count()
    return jsonify({"count": count})
