from flask import Flask, Blueprint, jsonify, request, send_from_directory, abort
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

from .models import db


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure the database
    instance_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "instance"
    )
    os.makedirs(instance_path, exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{os.path.join(instance_path, 'portfolio.db')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    # Import and register API blueprints
    from .routes import main as main_blueprint

    app.register_blueprint(main_blueprint, url_prefix="/api")

    # Define the absolute path to the frontend's public directory
    static_folder = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "public"
    )

    # Catch-all route to serve the multi-page frontend
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        if path == "":
            # Serve index.html for the root URL
            return send_from_directory(static_folder, "index.html")

        # Check if the requested path corresponds to an existing file
        if os.path.exists(os.path.join(static_folder, path)):
            return send_from_directory(static_folder, path)

        # Check if the path corresponds to a page by appending .html
        html_file_path = path + ".html"
        if os.path.exists(os.path.join(static_folder, html_file_path)):
            return send_from_directory(static_folder, html_file_path)

        # If nothing matches, return a 404 error
        abort(404)

    return app
