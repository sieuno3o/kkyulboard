from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
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
            pag = Post.query.order_by(Post.created_at.asc()).paginate(page=page, per_page=perPage)
        elif sort == 'recent':
            pag = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=perPage)
        elif sort == 'click':
            pag = Post.query.order_by(Post.click_count.desc()).paginate(page=page, per_page=perPage)
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
    comments = Comment.query.all()
    isLogin = True
    return render_template('board/detail.html', comments=comments, isLogin=isLogin)


@board_bp.route('/create')
def create():
    return render_template('board/create.html')


@board_bp.route('/get_comments')
def get_comments():
    comments = Comment.query.all()
    isLogin = True
    return jsonify(
        [{'username': comment.user.username, 'comments': comment.comments, 'updated_at': comment.updated_at.strftime("%Y-%m-%d %H:%M"),
          'is_login': isLogin} for comment
         in
         comments])


@board_bp.route('/add_comment', methods=['POST'])
def add_comments():
    '''
    게시판 -> 상세페이지 이동하여 페이지 번호 부여 받으면 해당 포스트 기준으로 작업할 예정
    - 현재는 임시 사용자, 포스트 내용 적용함
    '''
    comments = request.form.get('comments')
    if not comments:
        return

    user = User.query.first()
    if not user:
        user = User(username='이상일', password='1111', email='email2', grade='', userpic='')
        db.session.add(user)
        db.session.commit()
        user = User.query.first()

    post = Post.query.first()
    if not post:
        title = '백준 DFS'
        post = Post(title=title, body='body1', user_id=user.user_id, created_at=datetime.now(),
                    updated_at=datetime.now(), click_count=1)
        db.session.add(post)
        db.session.commit()
        post = Post.query.first()


    comment = Comment(comments=comments, user_id=user.user_id, post_id=post.post_id,
                      created_at=datetime.now(), updated_at=datetime.now())

    db.session.add(comment)
    db.session.commit()

    isLogin = True

    return jsonify({'username': comment.user.username, 'comments': comment.comments, 'updated_at': comment.updated_at.strftime("%Y-%m-%d %H:%M"),
                    'is_login': isLogin})

@board_bp.route('/test_data', methods=['POST'])
def test_data():
    user = User.query.filter_by(username='이상일').first()
    if not user:
        user = User(username='이상일', password='1111', email='email2', grade='', userpic='')
        db.session.add(user)
        db.session.commit()

    # title = '백준 16564. 히오스 프로그래머'
    # title = '프로그래머스 42898. 등굣길'
    # title = 'SWEA 5658. 보물상자 비밀번호'
    title = '백준 DFS'
    post = Post(title=title, body='body1', user_id=user.user_id, created_at=datetime.now(),
                updated_at=datetime.now(), click_count=3)

    db.session.add(post)
    db.session.commit()

    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', None, type=str)

    perPage = 20

    # 사용자의 불순한 값 대비 코드
    try:
        if sort == 'old':
            pag = Post.query.order_by(Post.created_at.asc()).paginate(page=page, per_page=perPage)
        elif sort == 'recent':
            pag = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=perPage)
        elif sort == 'click':
            pag = Post.query.order_by(Post.click_count.desc()).paginate(page=page, per_page=perPage)
        else:
            pag = Post.query.paginate(page=page, per_page=perPage)
    except:
        return redirect(url_for('board.index'))

    stIdx = (pag.page - 1) * pag.per_page + 1
    postsCount = min(pag.total, (page - 1) * perPage + len(pag.items))

    isLogin = current_user.is_authenticated
    return render_template('board/index.html', pag=pag, postsCount=postsCount, stIdx=stIdx, sort=sort, isLogin=isLogin)
