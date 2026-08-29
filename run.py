import os
from app import create_app, db
from app.utils.seeder import seed_database


# Determine environment configuration
config_name = os.environ.get(
    'FLASK_CONFIG', 
    'production' if os.environ.get('DATABASE_URL') else os.environ.get('FLASK_ENV', 'default')
)
app = create_app(config_name)

# Ensure database tables and initial seed data exist for Gunicorn production & development
with app.app_context():
    try:
        db.create_all()
        from app.models.user import User as UserModel
        if UserModel.query.count() == 0:
            seed_database()
    except Exception as e:
        app.logger.error(f"Database startup initialization error: {e}")

@app.cli.command('init-db')
def init_db():
    """Recreates database tables and seeds them with defaults."""
    db.drop_all()
    db.create_all()
    seed_database()
    print("Database initialized and seeded successfully.")

@app.cli.command('seed-db')
def seed_db():
    """Seeds the database with standard default items."""
    seed_database()
    print("Database seeded successfully.")

@app.shell_context_processor
def make_shell_context():
    from app.models import User, Page, Post, Event, Download, Setting
    return dict(db=db, User=User, Page=Page, Post=Post, Event=Event, Download=Download, Setting=Setting)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=(config_name == 'development' or config_name == 'default'))

