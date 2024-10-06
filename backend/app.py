from flask import Flask
from config import Config
from flask_cors import CORS
from models import db, migrate  # Import db and migrate from models

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Register Blueprints
    from routes.customer_routes import customer_bp
    from routes.admin_routes import admin_bp
    app.register_blueprint(customer_bp, url_prefix='/api/customer')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
