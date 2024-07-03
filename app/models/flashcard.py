#!/usr/bin/python3
""" This module defines the Flashcard class """


from app.models.base_model import BaseModel
# from app import db
from flask import current_app as app

db = app.storage.db

class Flashcard(BaseModel, db.Model):
    """ This class respresents flashcard in Flasheeta """
    __tablename__ = 'flashcards'
    question = db.Column(db.String(1024), nullable=False)
    answer = db.Column(db.String(1024), nullable=False)
    deck_id = db.Column(db.String(60), db.ForeignKey('decks.id'),
                        nullable=False)
    from app.models.progress import Progress
    progress = db.relationship('Progress', backref='flashcard',
                               cascade='all, delete-orphan')
