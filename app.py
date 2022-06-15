"""Blogly application."""

from flask import Flask
from models import db, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get('/')


@app.get('/users')

@app.get('/users/new')

@app.post('/users/new')

@app.get('/users/<user-id>')

@app.get('/users/<user-id>/edit')

@app.post('/users/<user-id>/edit')

@app.post('/users/<user-id>/delete')