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

    notices = Post.query.filter(Post.notice_mode==True).all()

    posts_query = Post.query.filter(Post.notice_mode!=True)
    if keyword:
        if cate == "title":
            posts_query = posts_query.filter(Post.title.like(f"%{keyword}%"))
        elif cate == "writer":
            posts_query = posts_query.join(User).filter(User.username == keyword)
        elif cate == "content":
            posts_query = posts_query.filter(Post.body.like(f"%{keyword}%"))

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
    return render_template('board/index.html', pag=pag, notices=notices, postsCount=postsCount, keyword=keyword, cate=cate, stIdx=stIdx, sort=sort, isLogin=isLogin)


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
            return redirect(request.referrer)

    # post_id에 해당하는 데이터가 없으면 index로 redirect
    if not post:
        flash("게시글이 존재하지 않습니다!", "info")
        return redirect(request.referrer)

    # click 카운트 추가
    post.click_count += 1
    db.session.commit()
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.asc()).all()

    # 로그인 사용자 정보 전달
    # 로그인되지 않은 경우 current_user가 None이기 때문에 따로 관리 필요
    userContext = {
        'id': -1,
        'grade': 0,
    }
    if current_user.is_authenticated:
        userContext['id'] = current_user.user_id
        userContext['grade'] = current_user.grade

    return render_template('board/detail.html', post=post, comments=comments, comCount=len(comments),
                           userContext=userContext)


@board_bp.route('/create', methods=["GET", "POST"])
def createPost():
    if request.method == "POST":
        # 폼에서 입력받은 정보
        title = request.form.get("title")
        secret = request.form.get("secretCheck")
        secret_bool = True if secret == 'on' else False
        notice_bool = False
        notice = request.form.get("noticeCheck")
        if notice:
            notice_bool = True if notice == 'on' else False
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
                    status=status, notice_mode=notice_bool,
                    created_at=created_at, updated_at=updated_at, click_count=click_count, like_count=like_count)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('board.index'))
    return render_template('board/create.html')

@board_bp.route('/delete/<int:post_id>')
def deletePost(post_id):
    post = Post.query.filter_by(post_id=post_id).first()
    
    if not post:
        flash("해당 게시글을 찾을 수 없습니다.", 'danger')
        return redirect(url_for('board.index'))
    
    if post.user != current_user:
        flash("삭제 권한이 없습니다.", 'danger')
        return redirect(url_for('board.index'))
    
    db.session.delete(post)
    db.session.commit()
    flash("게시글이 삭제되었습니다.", "success")
    return redirect(url_for('board.index'))



@board_bp.route('/edit/<int:post_id>', methods=["GET", "POST"])
def editPost(post_id):
    # 해당 ID의 게시글 찾기
    post = Post.query.filter_by(post_id=post_id).first()
    # 게시글이 존재하지 않으면 메인 페이지로 리디렉션
    if not post:
        flash("해당 게시글을 찾을 수 없습니다.", 'danger')
        return redirect(url_for('board.index'))
    # 현재 로그인한 사용자가 게시글의 작성자가 아니면 메인 페이지로 리디렉션
    if post.user != current_user:
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

@board_bp.route('/add_comment', methods=['POST'])
def add_comment():
    comments = request.form.get('comments')
    postId = request.referrer.split("/")[-1]
    if postId != request.form.get("postId"):
        flash("불법적인 접근은 인터넷 문화를 더럽힙니다!", "info")
        return redirect(request.referrer)
    userId = current_user.user_id
    comment = Comment(comments=comments, user_id=userId, post_id=postId,
                    created_at=datetime.now(), updated_at=datetime.now())
    db.session.add(comment)
    db.session.commit()
    return redirect(request.referrer)


@board_bp.route('/delete_comment', methods=['POST'])
def delete_comment():
    data = request.json
    comment_id = data.get("removeId")
    comment = Comment.query.filter(Comment.comment_id == comment_id).first()
    if comment:
        db.session.delete(comment)
        db.session.commit()
        flash("댓글이 삭제되었습니다", "info")
    return jsonify({'message': 'Comment deleted successfully'})


@board_bp.route('/update_comment', methods=['POST', 'GET'])
def update_comment():
    data = request.json
    if not data:
        print(f'data is null')
        return jsonify({'message': 'fail to update'})
    commentId = data['commentNo']
    content = data['commentData']
    comment = Comment.query.filter(Comment.comment_id == commentId).first()
    if comment:
        comment.comments = content
        db.session.commit()
    flash("댓글이 업데이트되었습니다", "info")
    return jsonify({'message': 'Comment deleted successfully'})

