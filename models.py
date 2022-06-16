"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()
DEFAULT_IMAGE_URL = "https://picsum.photos/id/237/200/300"


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User class that includes an id, the user's first name, last name,
    and an image url"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                           nullable=False)

    last_name = db.Column(db.String(50),
                          nullable=False)

    img_url = db.Column(db.String,
                        nullable=False,
                        default=DEFAULT_IMAGE_URL)

    posts = db.relationship('Post', backref='user')


class Post(db.Model):
    """Post class that includes an post id, the post's title, content,
    date-created-at timestamp, and a user-id"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(100),
                      nullable=False)

    content = db.Column(db.String(1500),
                        nullable=False)

    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=db.func.now())

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
