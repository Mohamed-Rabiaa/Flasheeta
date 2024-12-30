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
        old_user = User.query.filter_by(name=username).first()
        if old_user:
            flash('This username is already taken. Please choose a new one.')
        else:
            user = User(name=username)
            user.save()
            login_user(user)
            return redirect(url_for('decks.decks', user_id=user.id))
    else:
        if form.is_submitted():
            flash('Invalid username')

    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """
    Displays the login page and logs the user in if the form is validated.

    Returns:
        render_template: Renders 'login.html' template with the LoginForm object.
    """
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(name=username).first()
        if user:
            login_user(user)
            return redirect(url_for('decks.decks'))
        else:
            flash('Invalid username')

    return render_template('login.html', form=form)

@bp.route('/logout', strict_slashes=False)
@login_required
def logout():
    """
    Logs out the current user and redirects to the login page.

    Returns:
        redirect: Redirects to the 'login' route.
    """
    logout_user()
    get_flashed_messages(with_categories=True)
    return redirect(url_for('auth.login'))
