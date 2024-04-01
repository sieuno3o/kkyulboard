from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from ..database import *

board_bp = Blueprint('board', __name__, url_prefix='/board')


@board_bp.route('/index')
def index():
    return render_template('board/index.html')


@board_bp.route('/create')
def create():
    return render_template('board/create.html')

  

@board_bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', None, type=str)

    perPage = 20

    # 사용자의 불순한 값 대비 코드
    try:
        if sort == 'asc':
            pag = Post.query.order_by(Post.created_at.asc()).paginate(page=page, per_page=perPage)
        elif sort == 'desc':
            pag = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=perPage)
        else:
            pag = Post.query.paginate(page=page, per_page=perPage)
    except:
        return redirect(url_for('board.index'))

    stIdx = (pag.page - 1) * pag.per_page + 1
    postsCount = min(pag.total, (page - 1) * perPage + len(pag.items))

    return render_template('board/index.html', pag=pag, postsCount=postsCount, stIdx=stIdx, sort=sort)

# @board_bp.route('/recent', methods=['GET'])
# def recent():
#     posts_results = Post.query.order_by(Post.id.desc()).limit(20).all()
#     for post in posts_results:
#         post.updated_at = datetime.date(post.updated_at)

#     search_count = len(posts_results)
#     total_count = Post.query.count()
#     return render_template('board/index.html', posts=posts_results, search_count=search_count, total_count=total_count)


# @board_bp.route('/oldest', methods=['GET'])
# def oldest():
#     posts_results = Post.query.order_by(Post.id.asc()).limit(20).all()
#     for post in posts_results:
#         post.updated_at = datetime.date(post.updated_at)

#     search_count = len(posts_results)
#     total_count = Post.query.count()
#     return render_template('board/index.html', posts=posts_results, search_count=search_count, total_count=total_count)


@board_bp.route('/test_data', methods=['POST'])
def test_data():
    print('test')
    user = User.query.filter_by(username='user1').first()
    if not user:
        user = User(username='user1', password='1111', email='email1', grade='', userpic='')
        db.session.add(user)
        db.session.commit()

    post = Post(title='post1', body='body1', user_id=user.id, created_at=datetime.now(),
                updated_at=datetime.now(), click_count=1)

    db.session.add(post)
    db.session.commit()

    posts_results = Post.query.order_by(Post.id.desc()).limit(20).all()
    for post in posts_results:
        post.updated_at = datetime.date(post.updated_at)

    return render_template('board/index.html', posts=posts_results)

