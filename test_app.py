import unittest
from app import app, db, User

class BloglyTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'

        with app.app_context():
            db.create_all()
            user = User(first_name="Test", last_name="User", image_url=None)
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_user_listing(self):
        with self.client as c:
            resp = c.get('/users')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Test User', resp.data)

    def test_add_user(self):
        with self.client as c:
            resp = c.post('/users/new', data={'first_name': 'New', 'last_name': 'User', 'image_url': ''}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'New User', resp.data)

    def test_user_detail(self):
        with self.client as c:
            resp = c.get('/users/1')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Test User', resp.data)

    def test_edit_user(self):
        with self.client as c:
            resp = c.post('/users/1/edit', data={'first_name': 'Updated', 'last_name': 'User', 'image_url': ''}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Updated User', resp.data)

if __name__ == '__main__':
    unittest.main()

import unittest
from app import app, db, User, Post

class BloglyTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
        db.create_all()

        user = User(first_name="Test", last_name="User", image_url=None)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        with self.client as c:
            response = c.post('/users/new', data={'first_name': 'New', 'last_name': 'User', 'image_url': ''})
            self.assertEqual(response.status_code, 302)
            user = User.query.filter_by(first_name='New').first()
            self.assertIsNotNone(user)

    def test_show_user(self):
        with self.client as c:
            response = c.get('/users/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test User', response.data)

    def test_create_post(self):
        with self.client as c:
            response = c.post('/users/1/posts/new', data={'title': 'Test Post', 'content': 'Test Content'})
            self.assertEqual(response.status_code, 302)
            post = Post.query.filter_by(title='Test Post').first()
            self.assertIsNotNone(post)

    def test_show_post(self):
        with self.client as c:
            post = Post(title='Test Post', content='Test Content', user_id=1)
            db.session.add(post)
            db.session.commit()

            response = c.get(f'/posts/{post.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Post', response.data)

if __name__ == '__main__':
    unittest.main()