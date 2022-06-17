"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

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

    return render_template('users/list.html', users=users)


@app.get('/users/new')
def display_form_add_user():
    """Show form to add a user"""
    return render_template("users/add-user.html")


@app.post('/users/new')
def add_user():
    """Gather form info to create a new user, add to database, and return to list"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]
    img_url = img_url if img_url else None

    new_user = User(first_name=first_name,
                    last_name=last_name,
                    img_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:user_id>')
def display_user_page(user_id):
    """Show user page for desired user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/detail.html', user=user)


@app.get('/users/<int:user_id>/edit')
def display_form_edit_user(user_id):
    """Show edit form for the corresponding user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Get info from edit user info form, update database, and redirect to users"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]
    img_url = img_url if img_url else None

    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.img_url = img_url

    db.session.commit()

    return redirect("/users")


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete a user."""
    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:user_id>/posts/new')
def display_form_add_post(user_id):
    """Show form to add a new post"""
    user = User.query.get_or_404(user_id)
    return render_template("/posts/add-post.html", user=user)


@app.post('/users/<int:user_id>/posts/new')
def add_post(user_id):
    """Gather form info to create a new post, add to database, and return to user detail page."""
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title,
                    content=content,
                    user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.get('/posts/<int:post_id>')
def display_post_page(post_id):
    """Show desired post page"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/detail.html', post=post)


@app.get('/posts/<int:post_id>/edit')
def display_form_edit_post(post_id):
    """Show edit form for the corresponding post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)


@app.post('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Get info from edit post info form, update database, and redirect to posts"""
    post = Post.query.get_or_404(post_id)

    title = request.form["title"]
    content = request.form["content"]

    post.title = title
    post.content = content

    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete a post."""

    post = Post.query.get_or_404(post_id)
    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')
