#!/usr/bin/python3
"""
This module defines the User class.
"""

from app.models.base_model import BaseModel
from flask_login import UserMixin
from flask import current_app as app

db = app.storage.db

class User(BaseModel, db.Model, UserMixin):
    """
    This class represents a user in Flasheeta.

    Attributes:
        name (str): The name of the user, which is unique.
        decks (relationship): A relationship to the Deck model, representing decks owned by the user.
    """
    __tablename__ = 'users'
    name = db.Column(db.String(128), nullable=False, unique=True)

    from app.models.deck import Deck
    decks = db.relationship('Deck', backref='user', cascade="all, delete-orphan")
