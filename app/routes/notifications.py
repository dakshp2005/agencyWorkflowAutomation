from flask import Blueprint, jsonify, request
from app.services.notification_service import notification_service
from app.extensions import db

bp = Blueprint('notifications', __name__, url_prefix='/notifications')

@bp.route('/unread', methods=['GET'])
def get_unread():
    """Get unread notifications"""
    notifications = notification_service.get_unread_notifications()
    return jsonify({
        'notifications': [{
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'type': n.notification_type,
            'action_url': n.action_url,
            'created_at': n.created_at.isoformat()
        } for n in notifications],
        'count': len(notifications)
    })

@bp.route('/all', methods=['GET'])
def get_all():
    """Get all notifications"""
    notifications = notification_service.get_all_notifications()
    return jsonify({
        'notifications': [{
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'type': n.notification_type,
            'action_url': n.action_url,
            'is_read': n.is_read,
            'created_at': n.created_at.isoformat()
        } for n in notifications]
    })

@bp.route('/<int:id>/read', methods=['POST'])
def mark_read(id):
    """Mark a notification as read"""
    notification = notification_service.mark_as_read(id)
    if notification:
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Notification not found'}), 404

@bp.route('/mark-all-read', methods=['POST'])
def mark_all_read():
    """Mark all notifications as read"""
    notification_service.mark_all_as_read()
    return jsonify({'success': True})

@bp.route('/count', methods=['GET'])
def get_count():
    """Get unread notification count"""
    count = notification_service.get_unread_count()
    return jsonify({'count': count})
