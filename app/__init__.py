import os
from flask import Flask
from app.extensions import db, migrate, login_manager
from app.config import Config, DevelopmentConfig, ProductionConfig

def create_app(config_class=None):
    app = Flask(__name__)

    if config_class is None:
        config_class = ProductionConfig if os.getenv('FLASK_ENV') == 'production' else DevelopmentConfig

    app.config.from_object(config_class)

    import google.generativeai as genai
    genai.configure(api_key=app.config["GEMINI_API_KEY"])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.models import client, email_record, reply, meeting, document, rag_document, interaction_log, notification

    from app.routes.discovery import bp as discovery_bp
    from app.routes.dashboard import bp as dashboard_bp
    from app.routes.clients import bp as clients_bp
    from app.routes.emails import bp as emails_bp
    from app.routes.replies import bp as replies_bp
    from app.routes.meetings import bp as meetings_bp
    from app.routes.documents import bp as documents_bp
    from app.routes.api import bp as api_bp
    from app.routes.auth import bp as auth_bp
    from app.routes.notifications import bp as notifications_bp
    from app.routes.spa import spa

    app.register_blueprint(spa)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(clients_bp, url_prefix='/clients')
    app.register_blueprint(emails_bp, url_prefix='/emails')
    app.register_blueprint(replies_bp, url_prefix='/replies')
    app.register_blueprint(meetings_bp, url_prefix='/meetings')
    app.register_blueprint(documents_bp, url_prefix='/documents')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp)
    app.register_blueprint(discovery_bp)
    app.register_blueprint(notifications_bp)

    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @app.before_request
    def require_login():
        from flask import request
        from flask_login import current_user
        spa_endpoints = ['spa.login_page', 'spa.login', 'spa.register', 'spa.dashboard',
                         'spa.dashboard_stats', 'spa.get_clients', 'spa.create_client',
                         'spa.get_client', 'spa.update_client', 'spa.delete_client',
                         'spa.get_emails', 'spa.get_meetings', 'spa.get_documents',
                         'spa.get_leads', 'spa.get_activity', 'spa.get_notifications',
                         'spa.notification_count', 'spa.logout']
        if request.endpoint in spa_endpoints:
            return
        allowed_endpoints = ['auth.login', 'auth.signup', 'static']
        if not current_user.is_authenticated and request.endpoint not in allowed_endpoints:
            return login_manager.unauthorized()

    return app
