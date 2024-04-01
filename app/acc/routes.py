from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..utils import sha512_hash
from ..database import User
from flask_login import login_user, logout_user

acc_bp = Blueprint('acc', __name__, url_prefix='/acc')

@acc_bp.route('/index')
def index():
    return render_template('acc/index.html')

@acc_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("userid")
        userpass = request.form.get("userpw")
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == sha512_hash(userpass):
                flash('환영합니다!', 'success')
                login_user(user)
                return redirect(url_for('acc.index'))
            else:
                flash('아이디나 패스워드를 확인해주세요!', 'danger')
        else:
            flash('아이디나 패스워드를 확인해주세요!', 'danger')
    return render_template('acc/login.html')

@acc_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('acc.index'))