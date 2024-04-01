from flask import Blueprint, render_template

board_bp = Blueprint('board', __name__, url_prefix='/board')

@board_bp.route('/index')
def index():
    return render_template('board/index.html')