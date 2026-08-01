from flask import Flask
from flask_cors import CORS
from config.settings import SECRET_KEY, DEBUG
from config.database import init_db, close_db
from utils.error_handler import register_error_handlers
from routes.api_routes import api_bp

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DEBUG"] = DEBUG
    CORS(app)

    # Initialize Database
    init_db(app)

    # Register Error Handlers
    register_error_handlers(app)

    # Register Routes
    app.register_blueprint(api_bp)
    
    # Register DB teardown
    app.teardown_appcontext(close_db)

    return app

if __name__ == "__main__":
    app = create_app()
    print("=" * 50)
    print("SERVIDOR INICIADO")
    print(f"Rodando em http://localhost:5000 (DEBUG={DEBUG})")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)
