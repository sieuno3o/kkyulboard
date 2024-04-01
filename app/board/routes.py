import flask
import kkyulboard.app.database
from datetime import datetime
from flask import Blueprint, render_template
from ..database import *

board_bp = Blueprint('board', __name__, url_prefix='/board')


@board_bp.route('/index')
def index():
    posts_results = Post.query.all()
    for post in posts_results:
        post.updated_at = datetime.date(post.updated_at)
    return render_template('board/index.html', posts=posts_results)


@board_bp.route('/recent', methods=['GET'])
def recent():
    posts_results = Post.query.all()
    return render_template('board/index.html', posts=posts_results)


@board_bp.route('/oldest', methods=['GET'])
def oldest():
    posts_results = Post.query.all()
    return render_template('board/index.html', posts=posts_results)

@board_bp.route('/write', methods=['POST'])
def write():
    return render_template('board/index.html')

@board_bp.route('/test_data', methods=['POST'])
def test_data():
    print('test')
    user = User.query.filter_by(username='user1').first()
    if not user:
        user = User(username='user1', password='1111', email='email1', grade='', userpic='')
        db.session.add(user)
        db.session.commit()

    post = Post(title='post1', body='body1', user_id=user.id, created_at=datetime.now(),
                updated_at=datetime.now(), click_count=1)

    db.session.add(post)
    db.session.commit()

    posts_results = Post.query.all()

    return render_template('board/index.html', posts=posts_results)
