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
    """Show list of users as homepage"""
    return redirect("/users")

@app.get('/users')
def display_users():
    """Show list of users"""
    users = User.query.all()

    return render_template('list.html', users=users)

@app.get('/users/new')
def display_form_add_user():
    """Show form to add a user"""
    return render_template("form.html")

@app.post('/users/new')
def add_user():
    """Gather form info to create a new user, add to database, and return to list"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]

    new_user = User(first_name=first_name,
                    last_name=last_name,
                    img_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def display_user_page(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('detail.html', user=user)

@app.get('/users/<int:user_id>/edit')
def display_form_edit_user(user_id):

    user = User.query.get_or_404(user_id)

    return render_template('edit.html', user = user)

# @app.post('/users/<int:user_id>/edit')

# @app.post('/users/<int:user_id>/delete')