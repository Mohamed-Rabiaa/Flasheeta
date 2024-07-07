#!/usr/bin/python3
"""
register module

This module contains the RegisterForm class used in the registration page of the application.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    """
    This class represents the form used for user registration on the registration page.

    Attributes:
        username (StringField): A field for entering the username, with a data required validator.
        submit (SubmitField): A submit button for the form.
    """
    username = StringField('Enter Your Name:', validators=[DataRequired()])
    submit = SubmitField('Register')
