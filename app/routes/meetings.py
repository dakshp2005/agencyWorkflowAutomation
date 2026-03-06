from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.meeting import Meeting
from app.models.client import Client
from app.services.scheduler_service import scheduler_service
from app.services.notification_service import notification_service
from app.extensions import db
import json

bp = Blueprint('meetings', __name__)

@bp.route('/')
def index():
    meetings = Meeting.query.order_by(Meeting.created_at.desc()).all()
    return render_template('meetings/index.html', meetings=meetings)

@bp.route('/new')
def new():
    clients = Client.query.order_by(Client.name).all()
    return render_template('meetings/new.html', clients=clients)

@bp.route('/create', methods=['POST'])
def create():
    client_id = request.form.get('client_id')
    agenda = request.form.get('agenda')
    slots = request.form.get('proposed_slots')
    
    if not client_id or not agenda:
        flash('Client and agenda are required.', 'error')
        return redirect(url_for('meetings.new'))
    
    # Parse proposed slots (comma-separated datetime strings)
    proposed_slots = []
    if slots:
        proposed_slots = [s.strip() for s in slots.split(',') if s.strip()]
    
    meeting = Meeting(
        client_id=client_id,
        agenda=agenda,
        proposed_slots=proposed_slots,
        status='proposed'
    )
    db.session.add(meeting)
    db.session.commit()
    
    # Create notification
    client = Client.query.get(client_id)
    notification_service.notify_meeting_created(meeting.id, client.name)
    
    flash('Meeting created successfully!', 'success')
    return redirect(url_for('meetings.detail', id=meeting.id))

@bp.route('/<int:id>')
def detail(id):
    meeting = Meeting.query.get_or_404(id)
    return render_template('meetings/detail.html', meeting=meeting)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    meeting = Meeting.query.get_or_404(id)
    
    if request.method == 'POST':
        meeting.agenda = request.form.get('agenda')
        slots = request.form.get('proposed_slots')
        
        if slots:
            meeting.proposed_slots = [s.strip() for s in slots.split(',') if s.strip()]
        
        db.session.commit()
        flash('Meeting updated successfully.', 'success')
        return redirect(url_for('meetings.detail', id=meeting.id))
    
    clients = Client.query.order_by(Client.name).all()
    return render_template('meetings/edit.html', meeting=meeting, clients=clients)

@bp.route('/<int:id>/confirm', methods=['POST'])
def confirm(id):
    slot = request.form['slot']
    try:
        scheduler_service.confirm_meeting(id, slot)
        flash("Meeting confirmed successfully.", "success")
    except Exception as e:
        flash(f"Error confirming meeting: {str(e)}", "error")
    return redirect(url_for('meetings.detail', id=id))

@bp.route('/<int:id>/cancel', methods=['POST'])
def cancel(id):
    meeting = Meeting.query.get_or_404(id)
    meeting.status = 'cancelled'
    db.session.commit()
    flash("Meeting cancelled.", "warning")
    return redirect(url_for('meetings.index'))

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    meeting = Meeting.query.get_or_404(id)
    db.session.delete(meeting)
    db.session.commit()
    flash("Meeting deleted.", "info")
    return redirect(url_for('meetings.index'))
