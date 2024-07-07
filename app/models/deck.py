#!usr/bin/python3
""" This module defines the Deck class """

from app.models.base_model import BaseModel
from flask import current_app as app

db = app.storage.db

class Deck(BaseModel, db.Model):
    """
    This class represents a deck in Flasheeta.

    Attributes:
        name (str): The name of the deck.
        description (str): A brief description of the deck.
        user_id (str): The ID of the user who owns the deck.
        flashcards (relationship): A relationship to the Flashcard model.
    """
    __tablename__ = 'decks'
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    from app.models.flashcard import Flashcard
    flashcards = db.relationship('Flashcard', backref='deck',
                                 cascade='all, delete-orphan')
