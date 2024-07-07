#!/usr/bin/python3
"""
This module defines the Flashcard class.
"""

from app.models.base_model import BaseModel
from flask import current_app as app

db = app.storage.db

class Flashcard(BaseModel, db.Model):
    """
    This class represents a flashcard in Flasheeta.

    Attributes:
        question (str): The question or prompt on the flashcard.
        answer (str): The answer to the question on the flashcard.
        deck_id (str): The ID of the deck to which the flashcard belongs.
        progress (relationship): A relationship to the Progress model.
    """
    __tablename__ = 'flashcards'
    question = db.Column(db.String(1024), nullable=False)
    answer = db.Column(db.String(1024), nullable=False)
    deck_id = db.Column(db.String(60), db.ForeignKey('decks.id'), nullable=False)

    from app.models.progress import Progress
    progress = db.relationship('Progress', backref='flashcard', cascade='all, delete-orphan')
