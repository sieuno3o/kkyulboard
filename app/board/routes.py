from flask import Blueprint, render_template

board_bp = Blueprint('board', __name__, url_prefix='/board')


@board_bp.route('/index')
def index():
    return render_template('board/index.html')


@board_bp.route('/create_post')
def create_post():
    return render_template('board/create_post.html')
