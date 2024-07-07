#!/usr/bin/python3
"""
This module defines the Progress class.
"""

from app.models.base_model import BaseModel
from datetime import datetime
from flask import current_app as app

db = app.storage.db

class Progress(BaseModel, db.Model):
    """
    This class represents the progress of a flashcard in Flasheeta.

    Attributes:
        review_count (int): The total number of times the flashcard has been reviewed.
        correct_count (int): The number of times the flashcard was answered correctly.
        last_review_date (datetime): The date and time of the last review.
        next_review_date (datetime): The date and time of the next scheduled review.
        difficulty_rating (str): The current difficulty rating of the flashcard.
        ease_factor (float): The ease factor used in spaced repetition algorithms.
        interval (int): The interval (in days) until the next review.
        flashcard_id (str): The ID of the flashcard associated with this progress record.
    """
    review_count = db.Column(db.Integer, nullable=False, default=0)
    correct_count = db.Column(db.Integer, nullable=False, default=0)
    last_review_date = db.Column(db.DateTime, default=datetime.utcnow())
    next_review_date = db.Column(db.DateTime, default=datetime.utcnow())
    difficulty_rating = db.Column(db.String(60), nullable=False, default='Again')
    ease_factor = db.Column(db.Float, nullable=False, default=2.5)
    interval = db.Column(db.Integer, nullable=False, default=1)
    flashcard_id = db.Column(db.String(60), db.ForeignKey('flashcards.id'), nullable=False)
