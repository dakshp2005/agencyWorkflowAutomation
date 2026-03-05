from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.meeting import Meeting
from app.services.scheduler_service import scheduler_service
from app.extensions import db

bp = Blueprint('meetings', __name__)

@bp.route('/')
def index():
    meetings = Meeting.query.order_by(Meeting.created_at.desc()).all()
    return render_template('meetings/index.html', meetings=meetings)

@bp.route('/<int:id>')
def detail(id):
    meeting = Meeting.query.get_or_404(id)
    return render_template('meetings/detail.html', meeting=meeting)

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
