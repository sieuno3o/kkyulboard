from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    grade = db.Column(db.String, default=0)
    userpic = db.Column(db.String)
    posts = relationship('Post', back_populates='user', lazy='joined')
    # posts = relationship('Post', back_populates='user', lazy='select')

    def __repr__(self):
        return f"{self.username} <{self.email}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String, nullable=True)
    problem_url = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    click_count = db.Column(db.Integer, nullable=True)
    like_count = db.Column(db.Integer, nullable=True)
    secret_mode = db.Column(db.Boolean, nullable=True)
    user = relationship('User', back_populates='posts', lazy='joined')
    # user = relationship('User', back_populates='posts', lazy='select')

    def __repr__(self):
        return f'post'
