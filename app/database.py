from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    grade = db.Column(db.Integer, default=0)
    userpic = db.Column(db.String)
    comment = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    posts = relationship('Post', back_populates='user', lazy='joined')
    comments = relationship('Comment', back_populates='user', lazy='joined')
    likes = relationship('Like', back_populates='user', lazy='joined')

    def get_id(self):
        return str(self.user_id)

    def __repr__(self):
        return f"{self.username} <{self.email}>"


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.user_id'), nullable=False)
    status = db.Column(db.String, nullable=True)
    problem_url = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    click_count = db.Column(db.Integer, nullable=True)
    like_count = db.Column(db.Integer, nullable=True)
    secret_mode = db.Column(db.Boolean, nullable=True)
    user = relationship('User', back_populates='posts', lazy='joined')
    comments = relationship('Comment', back_populates='post', lazy='joined', cascade='all, delete-orphan')
    likes = relationship('Like', primaryjoin="and_(Post.post_id==Like.post_id, Like.deleted==False)",
                         back_populates='post', lazy='joined', cascade='all, delete-orphan')
    notice_mode = db.Column(db.Boolean, default=0)

    def __repr__(self):
        return f"[{self.user}] {self.title}"


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comments = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.user_id'), nullable=False)
    post_id = db.Column(db.Integer, ForeignKey('post.post_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    post = relationship('Post', back_populates='comments', lazy='joined')
    user = relationship('User', back_populates='comments', lazy='joined')


class Like(db.Model):
    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('user.user_id'), nullable=False)
    post_id = db.Column(db.Integer, ForeignKey('post.post_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    post = relationship('Post', back_populates='likes', lazy='joined')
    user = relationship('User', back_populates='likes', lazy='joined')
