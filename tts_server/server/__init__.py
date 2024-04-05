from flask import Flask
from server.controllers import default_controller


def create_app():
    """Create the Flask application"""
    app = Flask(__name__)

    with app.app_context():
        app.register_blueprint(default_controller.default_blueprint)

    return app
