import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        try:
            from flask_migrate import upgrade
            upgrade()
            print("Database migrated successfully.")
        except Exception as e:
            print(f"Error migrating database: {e}")
            
    app.run(debug=True, port=5000, use_reloader=False)
