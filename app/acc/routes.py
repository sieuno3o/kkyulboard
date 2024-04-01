from flask import Blueprint, render_template

acc_bp = Blueprint('acc', __name__, url_prefix='/acc')


@acc_bp.route('/index')
def index():
    return render_template('acc/index.html')


@acc_bp.route('/my_info')
def my_info():
    return render_template('acc/my_info.html')
