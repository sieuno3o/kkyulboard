from flask import Blueprint, render_template

acc_bp = Blueprint('acc', __name__, url_prefix='/acc')

@acc_bp.route('/index')
def index():
    return render_template('acc/index.html')