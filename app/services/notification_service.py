"""Service for managing notifications"""
from app.models.notification import Notification
from app.extensions import db
from flask import url_for

class NotificationService:
    
    def create_notification(self, title: str, message: str, notification_type: str, 
                          related_id: int = None, related_type: str = None, action_url: str = None):
        """Create a new notification"""
        notification = Notification(
            title=title,
            message=message,
            notification_type=notification_type,
            related_id=related_id,
            related_type=related_type,
            action_url=action_url
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    
    def get_unread_notifications(self, limit=10):
        """Get unread notifications"""
        return Notification.query.filter_by(is_read=False)\
            .order_by(Notification.created_at.desc())\
            .limit(limit).all()
    
    def get_all_notifications(self, limit=50):
        """Get all notifications"""
        return Notification.query.order_by(Notification.created_at.desc())\
            .limit(limit).all()
    
    def mark_as_read(self, notification_id):
        """Mark a notification as read"""
        notification = Notification.query.get(notification_id)
        if notification:
            notification.is_read = True
            db.session.commit()
        return notification
    
    def mark_all_as_read(self):
        """Mark all notifications as read"""
        Notification.query.filter_by(is_read=False).update({'is_read': True})
        db.session.commit()
    
    def get_unread_count(self):
        """Get count of unread notifications"""
        return Notification.query.filter_by(is_read=False).count()
    
    # Helper methods for creating specific notification types
    def notify_email_approval_required(self, email_id: int, client_name: str, subject: str):
        """Create notification for email approval"""
        return self.create_notification(
            title=f"Email Approval Required",
            message=f"Email to {client_name}: '{subject}' is pending approval",
            notification_type="email_approval",
            related_id=email_id,
            related_type="email",
            action_url=url_for('emails.detail', id=email_id)
        )
    
    def notify_document_approval_required(self, document_id: int, client_name: str, doc_title: str):
        """Create notification for document approval"""
        return self.create_notification(
            title=f"Document Approval Required",
            message=f"Document '{doc_title}' for {client_name} is ready for review",
            notification_type="document_approval",
            related_id=document_id,
            related_type="document",
            action_url=url_for('documents.detail', id=document_id)
        )
    
    def notify_meeting_created(self, meeting_id: int, client_name: str):
        """Create notification for new meeting"""
        return self.create_notification(
            title=f"Meeting Created",
            message=f"New meeting scheduled with {client_name}",
            notification_type="meeting_created",
            related_id=meeting_id,
            related_type="meeting",
            action_url=url_for('meetings.detail', id=meeting_id)
        )
    
    def notify_reply_received(self, reply_id: int, client_name: str):
        """Create notification for new reply"""
        return self.create_notification(
            title=f"New Reply Received",
            message=f"Reply received from {client_name}",
            notification_type="reply_received",
            related_id=reply_id,
            related_type="reply",
            action_url=url_for('replies.index')
        )

notification_service = NotificationService()
