#!/usr/bin/python3
"""
Routes for user authentication (login, logout, register) in Flasheeta.
"""

from app.models.user import User
from flask import (
    current_app as app, render_template, request, redirect, url_for, flash, get_flashed_messages, Blueprint
)
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from flask_login import login_user, logout_user, login_required, current_user

storage = app.storage

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """
    Displays the register page and adds the new user to the database if the form is validated.

    Returns:
        render_template: Renders 'register.html' template with the RegisterForm object.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Check if username already exists
        old_user = User.query.filter_by(name=username).first()
        if old_user:
            flash('This username is already taken. Please choose a new one.')
            return render_template('register.html', form=form)
        
        # Create new user with hashed password
        user = User(name=username)
        user.set_password(password)
        user.save()
        login_user(user)
        return redirect(url_for('decks.decks', user_id=user.id))

    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """
    Displays the login page and logs the user in if the form is validated.
    Clears any stale flash messages on GET requests.

    Returns:
        render_template: Renders 'login.html' template with the LoginForm object.
    """
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(name=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('decks.decks'))
        else:
            flash('Invalid username or password')
    else:
        # Clear any stale flash messages when displaying the login form (GET request)
        if request.method == 'GET':
            get_flashed_messages()

    return render_template('login.html', form=form)

@bp.route('/logout', strict_slashes=False)
@login_required
def logout():
    """
    Logs out the current user and redirects to the login page.
    Clears any existing flash messages before logout.

    Returns:
        redirect: Redirects to the 'login' route.
    """
    # Clear all flash messages before logout
    get_flashed_messages()
    logout_user()
    return redirect(url_for('auth.login'))
