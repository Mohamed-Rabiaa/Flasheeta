#!/usr/bin/python3
""" login module """


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    """
    This class represents the login form that we use in the login page
    """
    username = StringField('Enter Your Name:', validators=[DataRequired()])
    submit = SubmitField('Login')
