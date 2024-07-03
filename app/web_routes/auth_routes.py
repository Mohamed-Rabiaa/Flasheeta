#!/usr/bin/python3
""" Displays the login page """


from app.models.user import User
from flask import (current_app as app, render_template, request, redirect,
                url_for, flash, get_flashed_messages, Blueprint)
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from flask_login import login_user, logout_user, login_required, current_user
import os

storage = app.storage

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'],
           strict_slashes=False)
def register():
    """ Displays the register page and adds the new user to the database """
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        # Querying the database to check if there is an old user with the same username
        old_user = User.query.filter_by(name=username).first()
        if old_user:
            flash('This name is already taken, Please choose a new name')
        else:
            user = User(name= username)
            user.save()
            login_user(user)
            return redirect(url_for('decks.decks', user_id=user.id))
    else:
        if form.is_submitted():
            flash('Invalid username')

    return render_template('register.html', form=form)




@bp.route('/login', methods=['GET', 'POST'],
           strict_slashes=False)
def login():
    """ Displays the login page, query the user in the database
    and redirects him to the decks page if he has a valid username """
    form = LoginForm()
    app.logger.info('The form has been created')

    if form.validate_on_submit():
        app.logger.info('The form has been submitted and validated')
        username = form.username.data
        user = User.query.filter_by(name=username).first()
        if user:
            login_user(user)
            app.logger.info('The user has logged in')
            return redirect(url_for('decks.decks', user_id=user.id))
        else:
            app.logger.info("Invalid Username")
            flash('Invalid username')

    return render_template('login.html', form=form)

@bp.route('/logout', strict_slashes=False)
@login_required
def logout():
    """ Logout the user and redirects him to the login page """
    logout_user()
    get_flashed_messages(with_categories=True)
    return redirect(url_for('auth.login'))

'''
@app.teardown_appcontext
def teardown_appcontext(exception=None):
    # if current_user.is_authenticated:
    logout_user()


if __name__ == '__main__':
    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        raise ValueError("No SECRET_KEY set for Flask application")

    app.run(host='0.0.0.0', port=5000)
'''

