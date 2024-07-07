#!/usr/bin/python3
"""
new_flashcard module

This module contains the NewFlashcardForm class used in the new flashcard page of the application.
"""

from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class NewFlashcardForm(FlaskForm):
    """
    This class represents the form used to create new flashcards on the new flashcard page.

    Attributes:
        deck (SelectField): A dropdown field to select the deck for the new flashcard.
        front (TextAreaField): A text area field for the front side of the flashcard, required.
        back (TextAreaField): A text area field for the back side of the flashcard, required.
        submit (SubmitField): A submit button to add the new flashcard.
    """
    deck = SelectField('Deck')
    front = TextAreaField('Front', validators=[DataRequired()])
    back = TextAreaField('Back', validators=[DataRequired()])
    submit = SubmitField('Add')
