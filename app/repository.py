from .database import *
from ..app import *


class UserRepository:
    def __init__(self, app):
        self.app = app

    def save(self, user):
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

    def saveAll(self, users: list):
        with self.app.app_context():
            db.session.add_all(users)
            db.session.commit()

    def findAll(self) -> User:
        with self.app.app_context():
            return User.query.all()

    def findFirst(self) -> User:
        with self.app.app_context():
            return User.query.first()


class PostRepository:
    def __init__(self, app):
        self.app = app

    def save(self, post):
        with self.app.app_context():
            db.session.add(post)
            db.session.commit()

    def saveAll(self, posts: list):
        with self.app.app_context():
            db.session.add_all(posts)
            db.session.commit()

    def findAll(self) -> list[Post]:
        with self.app.app_context():
            return Post.query.all()

    def findFirst(self) -> Post:
        with self.app.app_context():
            return Post.query.first()

    def delete(self, postId: int):
        with self.app.app_context():
            comment = Post.query.filter(Post.post_id == postId).first()
            if comment:
                db.session.delete(comment)
                db.session.commit()


class CommentRepository:
    def __init__(self, app):
        self.app = app

    def save(self, comment: Comment):
        with self.app.app_context():
            db.session.add(comment)
            db.session.commit()

    def saveAll(self, comments: list[Comment]):
        with self.app.app_context():
            db.session.add_all(comments)
            db.session.commit()

    def findAll(self) -> list[Comment]:
        with self.app.app_context():
            return Comment.query.all()

    def findFirst(self) -> Comment:
        with self.app.app_context():
            return Comment.query.first()

    def delete(self, commentId: int):
        with self.app.app_context():
            comment = Comment.query.filter(Comment.comment_id == commentId).first()
            if comment:
                db.session.delete(comment)
                db.session.commit()

    def updateComments(self, commentId: int, comments: str):
        with self.app.app_context():
            comment = Comment.query.filter(Comment.comment_id == commentId).first()
            if comment:
                comment.comments = comments
                db.session.commit()
