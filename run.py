from app import create_app
from app.config import DevelopmentConfig
from scheduler import start_scheduler

app = create_app(DevelopmentConfig)
start_scheduler(app)

if __name__ == '__main__':
    with app.app_context():
        try:
            from flask_migrate import upgrade
            upgrade()
            print("Database migrated successfully.")
        except Exception as e:
            print(f"Error migrating database: {e}")
            
    app.run(debug=True, port=5000, use_reloader=False)
