#!/usr/bin/python3
""" This module defines the Progress class """


from app.models.base_model import BaseModel
from datetime import datetime
# from app import db

from flask import current_app as app

db = app.storage.db

class Progress(BaseModel, db.Model):
    """ This class represents progress of a flashcard in Flasheeta """
    review_count = db.Column(db.Integer, nullable=False, default=0)
    correct_count = db.Column(db.Integer, nullable=False, default=0)
    last_review_date = db.Column(db.DateTime, default=datetime.utcnow())
    next_review_date = db.Column(db.DateTime, default=datetime.utcnow())
    difficulty_rating = db.Column(db.String(60), nullable=False, default='Again')
    ease_factor = db.Column(db.Float, nullable=False, default=2.5)
    interval = db.Column(db.Integer, nullable=False, default=1)
    flashcard_id = db.Column(db.String(60), db.ForeignKey('flashcards.id'), nullable=False)

    
