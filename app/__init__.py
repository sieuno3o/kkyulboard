from flask import Flask
from .database import db, User, Post, Comment
from .acc.routes import acc_bp
from .board.routes import board_bp
from .utils import read_from_json
from flask_login import LoginManager
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    admin = Admin(app)
    print(Post.__table__.columns.keys())
    class UserAdmin(ModelView):
        column_list = User.__table__.columns.keys()

    class PostAdmin(ModelView):
        column_list =  Post.__table__.columns.keys() + ["user"]
    
    class CommentAdmin(ModelView):
        column_list = Comment.__table__.columns.keys() + ["user", "post"]
    
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(PostAdmin(Post, db.session))
    admin.add_view(CommentAdmin(Comment, db.session))

    app.secret_key = read_from_json('secret.json')["SECRETKEY"]

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
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    
    app.register_blueprint(acc_bp)
    app.register_blueprint(board_bp)

    return app


