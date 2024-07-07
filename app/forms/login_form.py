#!/usr/bin/python3
"""
Login module

This module contains the LoginForm class used in the login page of the application.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    """
    This class represents the login form used on the login page.

    Attributes:
        username (StringField): A field for entering the username, with a data required validator.
        submit (SubmitField): A submit button for the form.
    """
    username = StringField('Enter Your Name:', validators=[DataRequired()])
    submit = SubmitField('Login')
