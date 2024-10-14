from flask import Flask, session
from config import Config
from flask_cors import CORS
from models import db, migrate
from flask_session import Session  # Add this import

import logging
import multiprocessing


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)  
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, supports_credentials=True)

    # Register Blueprints for routes
    from routes.customer_routes import customer_bp
    from routes.admin_routes import admin_bp
    app.register_blueprint(customer_bp, url_prefix='/api/customer')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    return app

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    multiprocessing.log_to_stderr(logging.DEBUG)
    app = create_app()
    app.run(debug=True, port=5001)
    
