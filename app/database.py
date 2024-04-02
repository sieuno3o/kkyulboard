from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    grade = db.Column(db.String, default=0)
    userpic = db.Column(db.String)
    posts = relationship('Post', back_populates='user', lazy='joined')
    comments = relationship('Comment', back_populates='user', lazy='joined')

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
