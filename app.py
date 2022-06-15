"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.get('/')
def display_home():
    return redirect("/users")

@app.get('/users')
def display_users():
    users = User.query.all()

    return render_template('list.html', users=users)

@app.get('/users/new')
def display_form_add_user():
    return render_template("form.html")

@app.post('/users/new')
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]

    new_user = User(first_name=first_name,
                    last_name=last_name,
                    image_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

# @app.get('/users/<user-id>')

# @app.get('/users/<user-id>/edit')

# @app.post('/users/<user-id>/edit')

# @app.post('/users/<user-id>/delete')