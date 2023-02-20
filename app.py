"""Blogly application."""
import os
from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from helpers import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
# db.create_all()

@app.route('/')
def root():
    """Shows a list of all users"""

    return redirect('/users')

@app.route('/users')
def users():
    """Shows a list of all users"""

    users = User.query.all()

    return render_template('users.html', users=users)

@app.route('/users/new')
def add_user_form():
    """Shows a form to add a user"""

    return render_template('add-user.html')

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Shows a form to edit a user"""

    user = User.query.get_or_404(user_id)

    return render_template('edit-user.html', user=user)

@app.route('/users/new', methods=["POST"])
def add_user_post():
    """Accepts form input, Adds a user to the database"""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)

    replace_user_values_empty_with_null(new_user)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user_post(user_id):

    user = User.query.get_or_404(user_id)

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]

    user.first_name = first_name
    user.last_name = last_name
    user.img_url = img_url

    replace_user_values_empty_with_null(user)

    # db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Dispalys details of one user"""

    user = User.query.get_or_404(user_id)

    return render_template("user-detail.html", user=user)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def user_delete(user_id):
    """Deletes a user"""

    user = User.query.filter_by(id = user_id).delete()
    db.session.commit()

    return redirect('/users')

