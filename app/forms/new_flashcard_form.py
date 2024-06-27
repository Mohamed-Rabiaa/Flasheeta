#!/usr/bin/python3
""" new_flashcard module """


from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class NewFlashcardForm(FlaskForm):
    """
    This class represents the new_flashcard form that we use in the new flashcard page
    """
    deck = SelectField('Deck')
    front = TextAreaField('Front', validators=[DataRequired()])
    back = TextAreaField('Back', validators=[DataRequired()])
    submit = SubmitField('Add')
