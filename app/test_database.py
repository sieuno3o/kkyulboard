import unittest
import os
from datetime import *
from .database import *
from ..app import *


class TestDomain(unittest.TestCase):
    dbname = 'test_database.db'
    app = None
    test_db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), dbname)

    def setUp(self):
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        self.app = create_app_with_dbname(self.dbname)

    def tearDown(self):
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_user(self):
        user = User(username='test', password='1234', email='email', grade='', userpic='')

        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

        with self.app.app_context():
            users = User.query.all()

        self.assertEqual(1, len(users))

    def test_posts(self):
        user1 = User(username='user1', password='1111', email='email1', grade='', userpic='')
        user2 = User(username='user2', password='1111', email='email2', grade='', userpic='')

        with self.app.app_context():
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()
            users = User.query.all()

        self.assertEqual(2, len(users))

        posts = [
            Post(title='post1', body='body1', user_id=users[0].user_id, created_at=datetime.now(),
                 updated_at=datetime.now()),
            Post(title='post2', body='body2', user_id=users[0].user_id, created_at=datetime.now(),
                 updated_at=datetime.now()),
            Post(title='post3', body='body3', user_id=users[1].user_id, created_at=datetime.now(), updated_at=datetime.now())
        ]

        with self.app.app_context():
            db.session.add_all(posts)
            db.session.commit()
            posts_results = Post.query.all()

        self.assertEqual(3, len(posts_results))
        self.assertEqual('user1', posts_results[0].user.username)
        self.assertEqual('user1', posts_results[1].user.username)
        self.assertEqual('user2', posts_results[2].user.username)

        with self.app.app_context():
            users = User.query.all()

        self.assertEqual(2, len(users[0].posts))
        self.assertEqual(1, len(users[1].posts))


if __name__ == '__main__':
    unittest.main()
