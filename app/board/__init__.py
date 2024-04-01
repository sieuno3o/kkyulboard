from flask import Flask
from .routes import board_bp

def init_app(app: Flask):
    app.register_blueprint(board_bp)
