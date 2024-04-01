from flask import Flask
from .database import db
from .acc.routes import acc_bp
from .board.routes import board_bp
import os

def create_app():
        app = Flask(__name__, template_folder='../templates')
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] =\
                'sqlite:///' + os.path.join(basedir, 'database.db')
        db.init_app(app)

        app.register_blueprint(acc_bp)
        app.register_blueprint(board_bp)

        return app