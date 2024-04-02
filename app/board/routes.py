import flask
import kkyulboard.app.database
from datetime import datetime
from flask import Blueprint, render_template, request
from ..database import *

board_bp = Blueprint('board', __name__, url_prefix='/board')


class PostContext:
    def __init__(self, posts, search_count, total_count, page_links):
        self.posts = posts
        self.search_count = search_count
        self.total_count = total_count
        self.page_links = page_links
        self.page_links_count = len(page_links)


class PostService:
    def __init__(self):
        self.cur_page = 1
        self.max_record = 20
        self.is_latest = True

    def find_posts(self):
        new_page = request.args.get('page')
        if new_page:
            self.cur_page = int(new_page)

        if self.cur_page <= 0:
            self.cur_page = 1

        offset = (self.cur_page - 1) * self.max_record

        if self.is_latest:
            posts = Post.query.order_by(Post.id.desc()).offset(offset).limit(self.max_record).all()
        else:
            posts = Post.query.order_by(Post.id.asc()).offset(offset).limit(self.max_record).all()

        for post in posts:
            post.updated_at = datetime.date(post.updated_at)

        search_count = len(posts)
        total_count = Post.query.count()

        total_page_count = (total_count // self.max_record) + 1

        page_links = []
        for i in range(1, total_page_count + 1):
            page_links.append(f'/board/index?page={i}&search={0}')

        return PostContext(posts, search_count, total_count, page_links)


service = PostService()


@board_bp.route('/index')
def index():
    context = service.find_posts()
    return render_template('board/index.html', context=context)


@board_bp.route('/recent', methods=['GET'])
def recent():
    service.is_latest = True
    context = service.find_posts()
    return render_template('board/index.html', context=context)


@board_bp.route('/oldest', methods=['GET'])
def oldest():
    service.is_latest = False
    context = service.find_posts()
    return render_template('board/index.html', context=context)


@board_bp.route('/write', methods=['POST'])
def write():
    # 글 작성 기능 추가할 것
    return render_template('board/index.html')


@board_bp.route('/test_data', methods=['POST'])
def test_data():
    user = User.query.filter_by(username='이상일').first()
    if not user:
        user = User(username='이상일', password='1111', email='email2', grade='', userpic='')
        db.session.add(user)
        db.session.commit()

    post = Post(title='post2', body='body1', user_id=user.id, created_at=datetime.now(),
                updated_at=datetime.now(), click_count=1)

    db.session.add(post)
    db.session.commit()

    context = service.find_posts()
    return render_template('board/index.html', context=context)
