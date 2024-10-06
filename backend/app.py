from flask import Flask
from config import Config
from flask_cors import CORS
from models import db, migrate
from flask_session import Session  # Add this import

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SESSION_TYPE'] = 'filesystem'  # Configure session type
    Session(app)  # Initialize server-side sessions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, supports_credentials=True)  # Allow credentials for sessions

    # Register Blueprints
    from routes.customer_routes import customer_bp
    app.register_blueprint(customer_bp, url_prefix='/api/customer')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
