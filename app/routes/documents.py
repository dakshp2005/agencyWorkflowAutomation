from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from app.models.document import Document
from app.models.client import Client
from app.services.document_service import document_service
from app.services.notification_service import notification_service
from app.extensions import db
from werkzeug.utils import secure_filename
import io

bp = Blueprint('documents', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'md', 'html'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    documents = Document.query.order_by(Document.created_at.desc()).all()
    return render_template('documents/index.html', documents=documents)

@bp.route('/new')
def new():
    clients = Client.query.order_by(Client.name).all()
    return render_template('documents/new.html', clients=clients)

@bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('documents.new'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('documents.new'))
    
    if not allowed_file(file.filename):
        flash('File type not allowed. Allowed: txt, pdf, doc, docx, md, html', 'error')
        return redirect(url_for('documents.new'))
    
    client_id = request.form.get('client_id')
    title = request.form.get('title')
    doc_type = request.form.get('doc_type', 'report')
    
    if not client_id or not title:
        flash('Client and title are required', 'error')
        return redirect(url_for('documents.new'))
    
    content = ""
    if file.filename.endswith(('.txt', '.md', '.html')):
        try:
            content = file.read().decode('utf-8')
        except:
            content = "Binary file - content not available for preview"
    else:
        content = "Binary file - content not available for preview"
    
    filename = secure_filename(file.filename)
    
    doc = Document(
        client_id=client_id,
        title=title,
        doc_type=doc_type,
        content=content,
        file_path=filename,
        status='draft'
    )
    db.session.add(doc)
    db.session.commit()
    
    flash('Document uploaded successfully!', 'success')
    return redirect(url_for('documents.detail', id=doc.id))

@bp.route('/<int:id>')
def detail(id):
    document = Document.query.get_or_404(id)
    import markdown
    html_content = markdown.markdown(document.content or '')
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
    if not doc.content:
        flash("No content available for download.", "error")
        return redirect(url_for('documents.detail', id=id))
    return send_file(
        io.BytesIO(doc.content.encode('utf-8')),
        mimetype='text/markdown',
        as_attachment=True,
        download_name=f"{doc.title or 'document'}.md"
    )

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    doc = Document.query.get_or_404(id)
    db.session.delete(doc)
    db.session.commit()
    flash("Document deleted successfully.", "info")
    return redirect(url_for('documents.index'))

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
