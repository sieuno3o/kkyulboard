from flask import Flask
from .routes import acc_bp

def init_app(app: Flask):
    app.register_blueprint(acc_bp)
