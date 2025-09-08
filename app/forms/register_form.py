#!/usr/bin/python3
"""
register module

This module contains the RegisterForm class used in the registration page of the application.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo

class RegisterForm(FlaskForm):
    """
    Form for registering a new user.

    Fields:
        username (StringField): User's name, required.
        password (PasswordField): User's password, required, must be at least 8 characters and include uppercase, lowercase, numbers, and special characters.
        submit (SubmitField): Button to submit the registration form.
    """
    username = StringField('Name:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[
        DataRequired(message="Password is required"),
        Length(min=8, message="Password must be at least 8 characters"),
        Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])',
            message="Password must contain uppercase, lowercase, numbers, and special characters"
        )
    ])
    confirm_password = PasswordField('Confirm Password:', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')
