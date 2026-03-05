from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from app.models.document import Document
from app.services.document_service import document_service
from app.extensions import db
import os

bp = Blueprint('documents', __name__)

@bp.route('/')
def index():
    documents = Document.query.order_by(Document.created_at.desc()).all()
    return render_template('documents/index.html', documents=documents)

@bp.route('/<int:id>')
def detail(id):
    document = Document.query.get_or_404(id)
    import markdown
    html_content = markdown.markdown(document.content)
    return render_template('documents/detail.html', document=document, html_content=html_content)

@bp.route('/<int:id>/approve', methods=['POST'])
def approve(id):
    doc = Document.query.get_or_404(id)
    doc.status = 'approved'
    db.session.commit()
    flash("Document approved.", "success")
    return redirect(url_for('documents.detail', id=id))

@bp.route('/<int:id>/download', methods=['GET'])
def download(id):
    doc = Document.query.get_or_404(id)
    if not os.path.exists(doc.file_path):
        flash("File not found on disk.", "error")
        return redirect(url_for('documents.detail', id=id))
    return send_file(doc.file_path, as_attachment=True)

@bp.route('/generate', methods=['POST'])
def generate():
    client_id = request.form.get('client_id')
    doc_type = request.form.get('doc_type', 'proposal')
    try:
        if doc_type == 'proposal':
            document_service.generate_proposal(client_id)
            flash("Proposal generation started.", "success")
        else:
            document_service.generate_report(client_id)
            flash("Report generated.", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
    return redirect(url_for('documents.index'))
