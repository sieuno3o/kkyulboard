from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from ..database import *

board_bp = Blueprint('board', __name__, url_prefix='/board')


@board_bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'recent', type=str)

    perPage = 20

    # 사용자의 불순한 값 대비 코드
    try:
        if sort == 'old':
            pag = Post.query.order_by(Post.created_at.asc()).paginate(
                page=page, per_page=perPage)
        elif sort == 'recent':
            pag = Post.query.order_by(Post.created_at.desc()).paginate(
                page=page, per_page=perPage)
        elif sort == 'click':
            pag = Post.query.order_by(Post.click_count.desc()).paginate(
                page=page, per_page=perPage)
        else:
            pag = Post.query.paginate(page=page, per_page=perPage)
    except:
        return redirect(url_for('board.index'))

    stIdx = (pag.page - 1) * pag.per_page + 1
    postsCount = min(pag.total, (page - 1) * perPage + len(pag.items))

    isLogin = current_user.is_authenticated
    return render_template('board/index.html', pag=pag, postsCount=postsCount, stIdx=stIdx, sort=sort, isLogin=isLogin)


@board_bp.route('/detail')
def detail():
    return render_template('board/detail.html')


@board_bp.route('/create', methods=["GET", "POST"])
def createPost():
    if request.method == "POST":
        title = request.form.get("title")
        secret = request.form.get("secretValue")
        secret_bool = True if secret == 'True' else False
        problemUrl = request.form.get("problemUrl")
        body = request.form.get("body")
        user_id = "작성자"  # 수정 필요
        status = "normal"
        created_at = datetime.now()
        updated_at = datetime.now()
        click_count = 0
        like_count = 0
        post = Post(title=title, body=body, problem_url=problemUrl, secret_mode=secret_bool, user_id=user_id, status=status,
                    created_at=created_at, updated_at=updated_at, click_count=click_count, like_count=like_count)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('board.index'))
    return render_template('board/create.html')


@board_bp.route('/test_data', methods=['POST'])
def test_data():
    user = User.query.filter_by(username='이상일').first()
    if not user:
        user = User(username='이상일', password='1111',
                    email='email2', grade='', userpic='')
        db.session.add(user)
        db.session.commit()

    # title = '백준 16564. 히오스 프로그래머'
    # title = '프로그래머스 42898. 등굣길'
    # title = 'SWEA 5658. 보물상자 비밀번호'
    title = '백준 DFS'
    post = Post(title=title, body='body1', user_id=user.id, created_at=datetime.now(),
                updated_at=datetime.now(), click_count=3)

    db.session.add(post)
    db.session.commit()

    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', None, type=str)

    perPage = 20

    # 사용자의 불순한 값 대비 코드
    try:
        if sort == 'old':
            pag = Post.query.order_by(Post.created_at.asc()).paginate(
                page=page, per_page=perPage)
        elif sort == 'recent':
            pag = Post.query.order_by(Post.created_at.desc()).paginate(
                page=page, per_page=perPage)
        elif sort == 'click':
            pag = Post.query.order_by(Post.click_count.desc()).paginate(
                page=page, per_page=perPage)
        else:
            pag = Post.query.paginate(page=page, per_page=perPage)
    except:
        return redirect(url_for('board.index'))

    stIdx = (pag.page - 1) * pag.per_page + 1
    postsCount = min(pag.total, (page - 1) * perPage + len(pag.items))

    isLogin = current_user.is_authenticated
    return render_template('board/index.html', pag=pag, postsCount=postsCount, stIdx=stIdx, sort=sort, isLogin=isLogin)
