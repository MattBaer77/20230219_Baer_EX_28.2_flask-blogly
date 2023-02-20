from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
# app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add semple user."""

        User.query.delete()

        user = User(first_name="TestFirstName", last_name="TestLastName", img_url="TestURL")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_root(self):
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302)
            # Maybe add more?

    def test_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstName', html)

    def test_add_user_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form action="/users/new" method="POST">', html)

    def test_edit_user_form(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<form action="/users/{self.user_id}/edit" method="POST">', html)

    def test_add_user_post(self):
        with app.test_client() as client:
            d = {
                "first_name":"TestAddFirst",
                "last_name":"TestAddLast",
                "img_url":"TestAddURL"
            }

            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestAddFirst", html)