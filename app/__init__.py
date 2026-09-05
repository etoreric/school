from pathlib import Path
from flask import Flask, render_template
from config import config
from app.extensions import db, login_manager, csrf

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Ensure instance folder and uploads folders exist
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    uploads_dir = Path(app.config['UPLOAD_FOLDER'])
    uploads_dir.mkdir(parents=True, exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register Context Processors
    @app.context_processor
    def inject_globals():
        from app.models.cms import Page
        from app.models.site import Setting
        
        def get_setting(key, default=''):
            try:
                setting = Setting.query.filter_by(key=key).first()
                if setting and setting.value:
                    return setting.value
                return default
            except Exception:
                return default

        def get_navbar_pages():
            try:
                return Page.query.filter_by(is_published=True).all()
            except Exception:
                return []

        def get_unread_messages_count():
            try:
                from app.models.cms import ContactMessage
                return ContactMessage.query.filter_by(is_read=False).count()
            except Exception:
                return 0

        def get_unread_notifications_count():
            return 0

        def get_unread_notifications():
            return []

        return dict(
            get_navbar_pages=get_navbar_pages,
            get_setting=get_setting,
            get_unread_messages_count=get_unread_messages_count,
            get_unread_notifications_count=get_unread_notifications_count,
            get_unread_notifications=get_unread_notifications
        )

    # Import Blueprints
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(500)
    def handle_error(error):
        error_code = getattr(error, 'code', 500)
        error_message = getattr(error, 'description', 'An unexpected error occurred.')
        return render_template('error.html', error_code=error_code, error_message=error_message), error_code

    return app
