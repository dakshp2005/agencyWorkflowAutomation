from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.email_record import EmailRecord
from app.services.email_service import email_service
from app.extensions import db

bp = Blueprint('emails', __name__)

@bp.route('/')
def index():
    status_filter = request.args.get('status')
    if status_filter:
        emails = EmailRecord.query.filter_by(status=status_filter).order_by(EmailRecord.created_at.desc()).all()
    else:
        emails = EmailRecord.query.order_by(EmailRecord.created_at.desc()).all()
    return render_template('emails/index.html', emails=emails, current_filter=status_filter)

@bp.route('/<int:id>')
def detail(id):
    email = EmailRecord.query.get_or_404(id)
    return render_template('emails/detail.html', email=email)

@bp.route('/<int:id>/approve', methods=['POST'])
def approve(id):
    try:
        email_service.approve_and_send(id)
        flash("Email approved and sent successfully.", "success")
    except Exception as e:
        flash(f"Error sending email: {str(e)}", "error")
    return redirect(url_for('emails.index'))

@bp.route('/<int:id>/reject', methods=['POST'])
def reject(id):
    email_service.reject_email(id)
    flash("Email rejected and returned to draft.", "info")
    return redirect(url_for('emails.index'))

@bp.route('/<int:id>/edit', methods=['POST'])
def edit(id):
    email = EmailRecord.query.get_or_404(id)
    email.subject = request.form['subject']
    email.body = request.form['body']
    db.session.commit()
    flash("Email updated.", "success")
    return redirect(url_for('emails.detail', id=id))
