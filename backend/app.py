from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)

    # Import models
    from routes.customer_routes import customer_bp
    from routes.admin_routes import admin_bp
    app.register_blueprint(customer_bp, url_prefix='/api/customer')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
