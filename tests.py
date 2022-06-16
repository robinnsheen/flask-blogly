from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

TEST_IMAGE_URL = "https://picsum.photos/id/307/200/300"

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(first_name="test_first",
                                    last_name="test_last",
                                    img_url=None)

        second_user = User(first_name="test_first_two", last_name="test_last_two",
                           img_url=None)

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

        test_post = Post(title="test_title",
                         content="test_content",
                         user_id=self.user_id)

        db.session.add_all([test_post])
        db.session.commit()

        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Test that the list of users shows"""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_form_add_user_shows(self):
        """Test that the form to add user appears"""

        with self.client as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertIn('Add user form', html)
            self.assertEqual(resp.status_code, 200)

    def test_redirection_for_add_user(self):
        """Test redirection when adding user"""
        with app.test_client() as client:
            resp = client.post("/users/new",
                               data={'first_name': 'test_first',
                                     'last_name': 'test_last',
                                     'img_url': DEFAULT_IMAGE_URL})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")

    def test_add_user_submit(self):
        """Test that a user is added and displays in users list"""
        with app.test_client() as client:
            resp = client.post("/users/new", follow_redirects=True,
                               data={'first_name': 'test_first',
                                     'last_name': 'test_last',
                                     'img_url': DEFAULT_IMAGE_URL})

            html = resp.get_data(as_text=True)

            self.assertIn('test_first test_last', html)
            self.assertEqual(resp.status_code, 200)

    def test_edit_user_submit(self):
        """Test that a user can edit data and display changes"""
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/edit', follow_redirects=True,
                               data={'first_name': 'test_new_first',
                                     'last_name': 'test_new_last',
                                     'img_url': TEST_IMAGE_URL})

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test_new_first test_new_last', html)

    def test_form_add_post_shows(self):
        """Test that the form to add post appears"""

        with self.client as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add post form', html)

            resp = client.get("/users/-1/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 404)

    def test_add_post_submit(self):
        """Test that a post is added"""
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/posts/new", follow_redirects=True,
                               data={'title': 'test_title',
                                     'content': 'test_content',
                                     'user_id': f'{self.user_id}'})

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test_title', html)

            resp = client.post("/users/-1/posts/new", follow_redirects=True,
                               data={'title': 'test_title',
                                     'content': 'test_content',
                                     'user_id': f'{self.user_id}'})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 404)

    def test_edit_post_submit(self):
        """Test that a post can be edited and displays changes"""
        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/edit", follow_redirects=True,
                               data={'title': 'new_test_title',
                                     'content': 'new_test_content'})

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('new_test_title', html)
            self.assertIn('new_test_content', html)

    def test_delete_post(self):
        """Test that a post can be deleted"""
        with app.test_client() as client:
            resp = client.post(
                f"/posts/{self.post_id}/delete", follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('test_title', html)
