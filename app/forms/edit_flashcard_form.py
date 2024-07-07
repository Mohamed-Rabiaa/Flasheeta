#!/usr/bin/python3
"""
edit_flashcard module

This module contains the EditFlashcardForm class used in the edit flashcard page of the application.
"""

from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class EditFlashcardForm(FlaskForm):
    """
    This class represents the form used to edit flashcards on the edit flashcard page.

    Attributes:
        deck (SelectField): A dropdown field to select the deck for the flashcard.
        front (TextAreaField): A text area field for the front side of the flashcard, required.
        back (TextAreaField): A text area field for the back side of the flashcard, required.
        submit (SubmitField): A submit button to confirm the changes.
    """
    deck = SelectField('Deck')
    front = TextAreaField('Front', validators=[DataRequired()])
    back = TextAreaField('Back', validators=[DataRequired()])
    submit = SubmitField('Confirm')
