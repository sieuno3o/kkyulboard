from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from ..utils import sha512_hash
from ..database import User, db
from datetime import datetime
from flask_login import login_user, logout_user, current_user

acc_bp = Blueprint('acc', __name__, url_prefix='/acc')


@acc_bp.route('/index')
def index():
    return render_template('acc/index.html')

@acc_bp.route('/profile')
def profile():
    return render_template('acc/profile.html')


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

@acc_bp.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get('regName')
        password = sha512_hash(request.form.get('regPass'))
        email = request.form.get('regMail')
        comment = request.form.get("regCom")
        if 'regPic' not in request.files:
            filePath = "/uploads/noimage.png"
        else:
            userpic = request.files['regPic']
            ext = userpic.filename.split(".")[-1]
            hashed_filename = sha512_hash(f"{username}UserPic{datetime.now()}") + f".{ext}"
            filePath = '/uploads/userpic/' + hashed_filename
            userpic.save(f"static{filePath}")
        user = User(username=username, password=password, email=email, userpic=filePath, comment=comment)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('acc.login'))
    return render_template('acc/signup.html')

@acc_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('acc.index'))

@acc_bp.route("/checkNameDup", methods=["POST"])
def checkNameDup():
    data = request.json
    existing_user = User.query.filter_by(username=data["username"]).first()
    if existing_user:
        return jsonify({"is_duplicate": True})  # 사용자 이름이 이미 존재함
    return jsonify({"is_duplicate": False})

@acc_bp.route("/checkMailDup", methods=["POST"])
def checkMailDup():
    data = request.json
    existing_mail = User.query.filter_by(email=data["email"]).first()
    if existing_mail:
        return jsonify({"is_duplicate": True})  # 사용자 이름이 이미 존재함
    return jsonify({"is_duplicate": False})