from flask import Flask
from .database import db, User, Post, Comment
from .acc.routes import acc_bp
from .board.routes import board_bp
from .utils import read_from_json
from flask_login import LoginManager
import os
from flask_cors import CORS

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    CORS(app)
    app.secret_key = read_from_json('secret.json')["SECRETKEY"]
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(Comment, db.session))

    # app.config['UPLOAD_FOLDER'] = 'uploads'

    # Flask-Login을 위한 설정
    loginManager = LoginManager()
    loginManager.init_app(app)

    @loginManager.user_loader
    def load_user(user_id):
        from .database import User
        return User.query.get(int(user_id))
        

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'database.db')
    db.init_app(app)

    app.register_blueprint(acc_bp)
    app.register_blueprint(board_bp)

    return app


