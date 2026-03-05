from flask import Blueprint, render_template, jsonify, request
from app.models.reply import InboundReply
from app.services.reply_classifier import reply_classifier

bp = Blueprint('replies', __name__)

@bp.route('/')
def index():
    replies = InboundReply.query.order_by(InboundReply.processed_at.desc()).all()
    return render_template('replies/index.html', replies=replies)

@bp.route('/fetch', methods=['POST'])
def fetch():
    try:
        res = reply_classifier.fetch_and_classify()
        if request.headers.get('Accept') == 'application/json':
            return jsonify({"status": "success", "count": len(res)})
        return redirect(url_for('replies.index'))
    except Exception as e:
        if request.headers.get('Accept') == 'application/json':
            return jsonify({"status": "error", "message": str(e)}), 500
        return redirect(url_for('replies.index'))
