#!/usr/bin/python3
""" register module """


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    """
    This class represents the register form that we use in the register page
    """
    username = StringField('Enter Your Name:', validators=[DataRequired()])
    submit = SubmitField('Register')
