#!/usr/bin/python3
""" edit_flashcard module """


from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class EditFlashcardForm(FlaskForm):
    """
    This class represents the edit_flashcard form that we use in the edit flashcard page
    """
    deck = SelectField('Deck')
    front = TextAreaField('Front', validators=[DataRequired()])
    back = TextAreaField('Back', validators=[DataRequired()])
    submit = SubmitField('Confirm')
