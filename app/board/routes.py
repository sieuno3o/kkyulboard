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

    # stIdx = (pag.page - 1) * pag.per_page + 1

    stIdx = pag.total - (pag.page - 1) * pag.per_page
    postsCount = min(pag.total, (page - 1) * perPage + len(pag.items))

    isLogin = current_user.is_authenticated
    return render_template('board/index.html', pag=pag, postsCount=postsCount, stIdx=stIdx, sort=sort, isLogin=isLogin)


@board_bp.route('/detail')
def detail():
    post_id = request.args.get('post_id', None, type=int)

    if post_id:
        return redirect(url_for('board.render_detail', post_id=post_id))
    else:
        return redirect(url_for('board.index'))


@board_bp.route('/detail/<post_id>')
def render_detail(post_id):
    post = Post.query.filter_by(post_id=post_id).first()

    # post_id에 해당하는 데이터가 없으면 index로 redirect
    if not post:
        return redirect(url_for('board.index'))

    # click 카운트 추가
    post.click_count += 1
    db.session.commit()

    isLogin = current_user.is_authenticated
    return render_template('board/detail.html', isLogin=isLogin, post=post)


@board_bp.route('/create', methods=["GET", "POST"])
def createPost():
    if request.method == "POST":
        title = request.form.get("title")
        secret = request.form.get("secretValue")
        secret_bool = True if secret == 'true' else False
        problemUrl = request.form.get("problemUrl")
        body = request.form.get("body")
        user_id = "작성자"  # 수정 필요
        status = "normal"
        created_at = datetime.now()
        updated_at = datetime.now()
        click_count = 0
        like_count = 0
        post = Post(title=title, body=body, problem_url=problemUrl, secret_mode=secret_bool, user_id=user_id,
                    status=status,
                    created_at=created_at, updated_at=updated_at, click_count=click_count, like_count=like_count)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('board.index'))
    return render_template('board/create.html')


@board_bp.route('/get_comments', methods=["GET"])
def get_comments():
    post_id = request.args.get('post_id', None, type=int)
    if not post_id:
        print('post_id is null')
        return redirect(url_for('board.index'))

    comments = Comment.query.filter_by(post_id=post_id)
    currentUserId = -1
    if current_user.is_authenticated:
        currentUserId = current_user.user_id

    return jsonify(
        [{'username': comment.user.username, 'comments': comment.comments,
          'updated_at': comment.updated_at.strftime("%Y-%m-%d %H:%M"),
          'is_login': current_user.is_authenticated, 'user_id': comment.user_id, 'current_user_id': currentUserId} for
         comment
         in
         comments])


@board_bp.route('/add_comment', methods=['POST'])
def add_comments():
    comments = request.form.get('comments')
    postId = request.form.get('post_id')
    userId = current_user.user_id
    if not comments or not postId:
        print(f'comments={comments}, post id={postId}')
        return

    comment = Comment(comments=comments, user_id=userId, post_id=postId,
                      created_at=datetime.now(), updated_at=datetime.now())

    db.session.add(comment)
    db.session.commit()

    currentUserId = -1
    if current_user.is_authenticated:
        currentUserId = current_user.user_id
    return jsonify({'username': comment.user.username, 'comments': comment.comments,
                    'updated_at': comment.updated_at.strftime("%Y-%m-%d %H:%M"),
                    'is_login': current_user.is_authenticated, 'user_id': userId, 'current_user_id': currentUserId})


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

    stIdx = pag.total - (pag.page - 1) * pag.per_page
    postsCount = min(pag.total, (page - 1) * perPage + len(pag.items))

    isLogin = current_user.is_authenticated
    return render_template('board/index.html', pag=pag, postsCount=postsCount, stIdx=stIdx, sort=sort, isLogin=isLogin)
