from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.client import Client
from app.extensions import db
from app.services.rag_service import rag_service

bp = Blueprint('clients', __name__)

@bp.route('/')
def index():
    status_filter = request.args.get('status')
    if status_filter:
        clients = Client.query.filter_by(status=status_filter).order_by(Client.created_at.desc()).all()
    else:
        clients = Client.query.order_by(Client.created_at.desc()).all()
    return render_template('clients/index.html', clients=clients, current_filter=status_filter)

@bp.route('/new', methods=['GET', 'POST'])
def new_client():
    if request.method == 'POST':
        if Client.query.filter_by(email=request.form['email']).first():
            flash('A client with this email already exists.', 'error')
            return redirect(url_for('clients.new_client'))
            
        c = Client(
            name=request.form['name'],
            email=request.form['email'],
            company=request.form.get('company'),
            industry=request.form.get('industry'),
            website=request.form.get('website'),
            phone=request.form.get('phone'),
            preferences=request.form.get('preferences'),
            notes=request.form.get('notes')
        )
        db.session.add(c)
        db.session.commit()
        
        text = f"Client: {c.name}, Company: {c.company}, Industry: {c.industry}, Preferences: {c.preferences}, Notes: {c.notes}"
        rag_service.add_document(text, c.id, "registration")
        flash('Client added successfully!', 'success')
        return redirect(url_for('clients.detail', id=c.id))
        
    return render_template('clients/new.html')

@bp.route('/<int:id>')
def detail(id):
    client = Client.query.get_or_404(id)
    return render_template('clients/detail.html', client=client)

@bp.route('/<int:id>/edit', methods=['POST'])
def edit(id):
    client = Client.query.get_or_404(id)
    client.name = request.form['name']
    client.company = request.form.get('company')
    client.industry = request.form.get('industry')
    client.website = request.form.get('website')
    client.phone = request.form.get('phone')
    client.preferences = request.form.get('preferences')
    client.notes = request.form.get('notes')
    db.session.commit()
    flash('Client updated.', 'info')
    return redirect(url_for('clients.detail', id=client.id))

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    client = Client.query.get_or_404(id)
    client.status = 'archived'
    db.session.commit()
    flash('Client archived.', 'warning')
    return redirect(url_for('clients.index'))
