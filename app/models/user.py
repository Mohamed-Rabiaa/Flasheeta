#!/usr/bin/python3
"""
This module defines the User class.
"""

from app.models.base_model import BaseModel
from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

db = app.storage.db

class User(BaseModel, UserMixin, db.Model):
    """
    Represents a user in the Flasheeta application.

    Attributes:
        name (str): Unique username of the user.
        email (str): Email address of the user.
        password_hash (str): Hashed password for authentication.
        decks (relationship): Relationship to Deck objects owned by the user.
    """
    __tablename__ = 'users'
    name = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def __init__(self, username=None, email=None, password_hash=None, **kwargs):
        """Initialize user with username, email, and pre-hashed password"""
        super().__init__(**kwargs)
        if username:
            self.name = username
        if email:
            self.email = email
        if password_hash:
            self.password_hash = password_hash

    from app.models.deck import Deck
    decks = db.relationship('Deck', backref='user', cascade="all, delete-orphan")

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)
