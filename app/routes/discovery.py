from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.lead import Lead
from app.services.discovery_service import discovery_service
from app.extensions import db

bp = Blueprint('discovery', __name__, url_prefix='/discovery')

@bp.route('/')
def index():
    leads = Lead.query.order_by(Lead.created_at.desc()).all()
    return render_template('discovery/index.html', leads=leads)

@bp.route('/search', methods=['POST'])
def search():
    domain = request.form.get('domain')
    if not domain:
        flash('Please enter a domain/industry to search for.', 'warning')
        return redirect(url_for('discovery.index'))
    
    flash(f"Searching for leads in '{domain}'...", 'info')
    leads = discovery_service.discover_leads(domain)
    if leads:
        flash(f"Successfully discovered {len(leads)} new prospects!", 'success')
    else:
        flash("Discovery failed or no results found.", 'error')
        
    return redirect(url_for('discovery.index'))

@bp.route('/qualify/<int:id>', methods=['POST'])
def qualify(id):
    from app.models.client import Client
    lead = Lead.query.get_or_404(id)
    
    # Convert lead to client
    client = Client(
        name=lead.name,
        company=lead.company,
        industry=lead.industry,
        website=lead.website,
        email=lead.email if lead.email else f"info@{lead.company.lower().replace(' ', '')}.com",
        notes=f"Discovered via AI Discovery ({lead.domain_topic}). ICP Reasoning: {lead.icp_reasoning}"
    )
    lead.status = 'qualified'
    db.session.add(client)
    db.session.commit()
    
    flash(f"{lead.company} has been qualified and added as a client.", 'success')
    return redirect(url_for('clients.detail', id=client.id))
