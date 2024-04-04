from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import current_user
from ..database import *
from flask import flash

board_bp = Blueprint('board', __name__, url_prefix='/board')


@board_bp.route('/index')
def index():
    cate = request.args.get('cate', "", type=str)
    keyword = request.args.get('keyword', "", type=str)
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'recent', type=str)

    perPage = 20

    if keyword:
        if cate == "title":
            posts_query = Post.query.filter(Post.title.like(f"%{keyword}%"))
        elif cate == "writer":
            posts_query = Post.query.join(User).filter(User.username == keyword)
        elif cate == "content":
            posts_query = Post.query.filter(Post.body.like(f"%{keyword}%"))
        else:
            posts_query = Post.query
    else:
        posts_query = Post.query

    if sort == 'old':
        posts_query = posts_query.order_by(Post.created_at.asc())
    elif sort == 'recent':
        posts_query = posts_query.order_by(Post.created_at.desc())
    elif sort == 'click':
        posts_query = posts_query.order_by(Post.click_count.desc())

    pag = posts_query.paginate(page=page, per_page=perPage)

    # stIdx = (pag.page - 1) * pag.per_page + 1

    stIdx = pag.total - (pag.page - 1) * pag.per_page
    postsCount = min(pag.total, (page - 1) * perPage + len(pag.items))

    isLogin = current_user.is_authenticated
    return render_template('board/index.html', pag=pag, postsCount=postsCount, keyword=keyword, cate=cate, stIdx=stIdx,
                           sort=sort, isLogin=isLogin)


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

    if post.secret_mode:
        if not (post.user_id == current_user.user_id or current_user.grade):
            flash("접근 권한이 없습니다!", "info")
            print(post.user_id, current_user.user_id)
            return redirect(request.referrer)
    # post_id에 해당하는 데이터가 없으면 index로 redirect
    if not post:
        flash("게시글이 존재하지 않습니다!", "info")
        return redirect(request.referrer)

    # click 카운트 추가
    post.click_count += 1
    db.session.commit()

    isLogin = current_user.is_authenticated
    return render_template('board/detail.html', isLogin=isLogin, post=post)


@board_bp.route('/create', methods=["GET", "POST"])
def createPost():
    if request.method == "POST":
        # 폼에서 입력받은 정보
        title = request.form.get("title")
        secret = request.form.get("secretValue")
        secret_bool = True if secret == 'true' else False
        problemUrl = request.form.get("problemUrl")
        body = request.form.get("body")

        # 현재 로그인한 사용자 ID
        user_id = current_user.user_id

        # 그 외 필요한 게시글 정보
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


@board_bp.route('/edit/<int:post_id>', methods=["GET", "POST"])
def editPost(post_id):
    # 해당 ID의 게시글 찾기
    post = Post.query.filter_by(post_id=post_id).first()

    # 게시글이 존재하지 않으면 메인 페이지로 리디렉션
    if not post:
        flash("해당 게시글을 찾을 수 없습니다.", 'danger')
        return redirect(url_for('board.index'))

    # 현재 로그인한 사용자가 게시글의 작성자가 아니면 메인 페이지로 리디렉션
    if post.user_id != current_user.user_id:
        flash("수정 권한이 없습니다.", 'danger')
        return redirect(url_for('board.index'))

    if request.method == "POST":
        # 폼에서 수정된 내용 가져오기
        title = request.form.get("title")
        secret = request.form.get("secretValue") == 'true'
        problemUrl = request.form.get("problemUrl")
        body = request.form.get("body")

        # 게시글 객체를 수정된 내용으로 업데이트
        post.title = title
        post.secret_mode = secret
        post.problem_url = problemUrl
        post.body = body
        post.updated_at = datetime.now()

        db.session.commit()

        flash("게시글이 수정되었습니다.", "success")
        return redirect(url_for('board.detail', post_id=post.post_id))

    # GET 요청시에는 수정 페이지를 렌더링
    return render_template('board/edit.html', post=post)


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
        [{'comment_id': comment.comment_id,
          'username': comment.user.username, 'comments': comment.comments,
          'updated_at': comment.updated_at.strftime("%Y-%m-%d %H:%M"),
          'is_login': current_user.is_authenticated, 'user_id': comment.user_id, 'current_user_id': currentUserId} for
         comment
         in
         comments])


@board_bp.route('/add_comment', methods=['POST'])
def add_comment():
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

    return jsonify({'comment_id': comment.comment_id,
                    'username': comment.user.username, 'comments': comment.comments,
                    'updated_at': comment.updated_at.strftime("%Y-%m-%d %H:%M"),
                    'is_login': current_user.is_authenticated})


@board_bp.route('/delete_comment/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.filter(Comment.comment_id == comment_id).first()
    if comment:
        db.session.delete(comment)
        db.session.commit()

    return jsonify({'message': 'Comment deleted successfully'})


@board_bp.route('/update_comment', methods=['POST', 'GET'])
def update_comment():
    data = request.json

    if not data:
        print(f'data is null')
        return jsonify({'message': 'fail to update'})

    commentId = data['id']
    content = data['content']

    comment = Comment.query.filter(Comment.comment_id == commentId).first()
    if comment:
        comment.comments = content
        db.session.commit()

    return jsonify({'message': 'Comment deleted successfully'})


@board_bp.route('/get_like', methods=['GET'])
def get_like():
    post_id = request.args.get('post_id', None, type=int)

    like_img = url_for('static', filename='icon/00_like.png')
    not_like_img = url_for('static', filename='icon/01_not_like.png')
    is_login = current_user.is_authenticated
    like_count = Like.query.filter_by(post_id=post_id, deleted=False).count()
    is_like = False
    if is_login:
        user_id = current_user.user_id
        like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if like:
            is_like = not like.deleted

    return jsonify({'like_img': like_img, 'not_like_img': not_like_img, 'is_login': is_login, 'like_count': like_count,
                    'is_like': is_like})


@board_bp.route('/set_like', methods=['POST'])
def set_like():
    data = request.json

    if not data:
        print(f'data is null')
        return jsonify({'message': 'fail to update'})

    is_login = current_user.is_authenticated
    if is_login == False:
        return jsonify({'message': 'fail to update'})

    user_id = current_user.user_id
    is_like = data['is_like']
    post_id = data['post_id']

    like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if like:
        like.deleted = not is_like
        like.updated_at = datetime.now()
        db.session.commit()
    else:
        like = Like(user_id=user_id, post_id=post_id, deleted=False, created_at=datetime.now(), updated_at=datetime.now())
        db.session.add(like)
        db.session.commit()

    like_img = url_for('static', filename='icon/00_like.png')
    not_like_img = url_for('static', filename='icon/01_not_like.png')
    like_count = Like.query.filter_by(post_id=post_id, deleted=False).count()
    is_like = not like.deleted

    return jsonify({'like_img': like_img, 'not_like_img': not_like_img, 'is_login': is_login, 'like_count': like_count,
                    'is_like': is_like})


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
