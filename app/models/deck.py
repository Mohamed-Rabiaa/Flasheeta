#!usr/bin/python3
""" This module defines the Deck class """


from app.models.base_model import BaseModel
from app import db

class Deck(BaseModel, db.Model):
    """ This class represents a deck in Flasheeta """
    __tablename__ = 'decks'
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    from app.models.flashcard import Flashcard
    flashcards = db.relationship('Flashcard', backref='deck',
                                 cascade='all, delete-orphan')
