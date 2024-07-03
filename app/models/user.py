#!/usr/bin/python3
""" This module defines the User class """


from app.models.base_model import BaseModel
from flask_login import UserMixin
# from app import db
from flask import current_app as app

db = app.storage.db

class User(BaseModel, db.Model, UserMixin):
    """ This class represents the user in Flasheeta """
    __tablename__ = 'users'
    name = db.Column(db.String(128), nullable=False, unique=True)
    from app.models.deck import Deck
    decks = db.relationship('Deck', backref='user',
                             cascade="all, delete-orphan")
    
