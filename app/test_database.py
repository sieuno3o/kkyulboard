import unittest
import os
from datetime import *
from .database import *
from ..app import *
from .repository import *


class TestDomain(unittest.TestCase):
    dbname = 'test_database.db'
    app = None
    test_db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), dbname)

    def setUp(self):
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        self.app = create_app_with_dbname(self.dbname)
        self.userRepo = UserRepository(self.app)
        self.postRepo = PostRepository(self.app)
        self.commentRepo = CommentRepository(self.app)

    def tearDown(self):
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_user(self):
        user = User(username='test', password='1234', email='email', grade='', userpic='')

        self.userRepo.save(user)

        user = self.userRepo.findFirst()

        self.assertIsNotNone(user)
        self.assertEqual(1, user.user_id)

    def test_posts(self):
        user1 = User(username='user1', password='1111', email='email1', grade='', userpic='')
        user2 = User(username='user2', password='1111', email='email2', grade='', userpic='')

        self.userRepo.saveAll([user1, user2])
        users = self.userRepo.findAll()

        self.assertEqual(2, len(users))

        posts = [
            Post(title='post1', body='body1', user_id=users[0].user_id, created_at=datetime.now(),
                 updated_at=datetime.now()),
            Post(title='post2', body='body2', user_id=users[0].user_id, created_at=datetime.now(),
                 updated_at=datetime.now()),
            Post(title='post3', body='body3', user_id=users[1].user_id, created_at=datetime.now(),
                 updated_at=datetime.now())
        ]

        self.postRepo.saveAll(posts)
        posts = self.postRepo.findAll()

        self.assertEqual(3, len(posts))
        self.assertEqual('user1', posts[0].user.username)
        self.assertEqual('user1', posts[1].user.username)
        self.assertEqual('user2', posts[2].user.username)

        users = self.userRepo.findAll()

        self.assertEqual(2, len(users[0].posts))
        self.assertEqual(1, len(users[1].posts))

        self.postRepo.delete(posts[0].post_id)
        posts = self.postRepo.findAll()

        self.assertEqual(2, len(posts))

    def test_comments_save_find_delete(self):
        users = [
            User(username='user1', password='1111', email='email1', grade='', userpic=''),
            User(username='user2', password='1111', email='email2', grade='', userpic='')
        ]
        self.userRepo.saveAll(users)

        users = self.userRepo.findAll()
        post = Post(title='post1', body='body1', user_id=users[0].user_id, created_at=datetime.now(),
                    updated_at=datetime.now())

        self.postRepo.save(post)

        post = self.postRepo.findFirst()

        comment1 = Comment(comments='comment1', user_id=users[0].user_id, post_id=post.post_id,
                           created_at=datetime.now(), updated_at=datetime.now())
        comment2 = Comment(comments='comment2', user_id=users[0].user_id, post_id=post.post_id,
                           created_at=datetime.now(), updated_at=datetime.now())
        comment3 = Comment(comments='comment3', user_id=users[1].user_id, post_id=post.post_id,
                           created_at=datetime.now(), updated_at=datetime.now())
        comment4 = Comment(comments='comment4', user_id=users[1].user_id, post_id=post.post_id,
                           created_at=datetime.now(), updated_at=datetime.now())

        self.commentRepo.saveAll([comment1, comment2, comment3, comment4])
        comments = self.commentRepo.findAll()
        self.assertEqual(4, len(comments))
        self.assertEqual('user1', comments[0].user.username)
        self.assertEqual('user1', comments[1].user.username)
        self.assertEqual('user2', comments[2].user.username)
        self.assertEqual('user2', comments[3].user.username)

        self.assertEqual('post1', comments[0].post.title)
        self.assertEqual('post1', comments[1].post.title)
        self.assertEqual('post1', comments[2].post.title)
        self.assertEqual('post1', comments[3].post.title)

        self.commentRepo.delete(comments[0].comment_id)
        comments = self.commentRepo.findAll()
        self.assertEqual(3, len(comments))

        self.postRepo.delete(post.post_id)
        comments = self.commentRepo.findAll()
        self.assertEqual(0, len(comments))

    def test_comments_update(self):
        user = User(username='user1', password='1111', email='email1', grade='', userpic='')
        self.userRepo.save(user)
        user = self.userRepo.findFirst()
        post = Post(title='post1', body='body1', user_id=user.user_id, created_at=datetime.now(),
                    updated_at=datetime.now())
        self.postRepo.save(post)
        post = self.postRepo.findFirst()

        comment1 = Comment(comments='comment1', user_id=user.user_id, post_id=post.post_id,
                           created_at=datetime.now(), updated_at=datetime.now())
        comment2 = Comment(comments='comment2', user_id=user.user_id, post_id=post.post_id,
                           created_at=datetime.now(), updated_at=datetime.now())

        self.commentRepo.saveAll([comment1, comment2])
        comments = self.commentRepo.findAll()

        self.commentRepo.updateComments(comments[0].comment_id, 'new_comment1')
        self.commentRepo.updateComments(comments[1].comment_id, 'new_comment2')

        comments = self.commentRepo.findAll()

        self.assertEqual('new_comment1', comments[0].comments)
        self.assertEqual('new_comment2', comments[1].comments)


if __name__ == '__main__':
    unittest.main()
