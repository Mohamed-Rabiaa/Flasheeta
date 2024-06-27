#!/usr/bin/python3
""" This module defines the Progress class """


from app.models.base_model import BaseModel
from app import db
from datetime import datetime

class Progress(BaseModel, db.Model):
    """ This class respresents progress of a flashcard in Flasheeta """
    review_count = db.Column(db.Integer, nullable=False, default=0)
    correct_count = db.Column(db.Integer, nullable=False, default=0)
    last_review_date = db.Column(db.DateTime, nullable=False,
                                 default=datetime.utcnow)
    flashcard_id = db.Column(db.String(60), db.ForeignKey('flashcards.id'),
                             nullable=False)
    
