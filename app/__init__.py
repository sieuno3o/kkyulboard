from flask import Flask
from .database import db
import os

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] =\
            'sqlite:///' + os.path.join(basedir, 'database.db')
    db.init_app(app)

    from .acc import init_app as acc_init_app
    acc_init_app(app)

    from .board import init_app as board_init_app
    board_init_app(app)

    return app