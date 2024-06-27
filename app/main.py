#!/usr/bin/python3

from models.base_model import app
from flask import Flask
from models.base_model import BaseModel, db
from models import *
from datetime import datetime

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        model = BaseModel()
        dct = {'name':'Ahmed Hussien'}
        user = user.User(**dct)
        storage.add(user)

        d = {'name':'English', 'description': 'English deck', 'user_id': 'c8b4bba1-4675-4a20-9766-b4786dc80bcd'}
        deck = deck.Deck(**d)
        storage.add(deck)

        f = {'question':'What does hello mean?', 'answer':'It\'s a greeting', 'deck_id': 'c8b4bba1-4675-4a20-9766-b4786dc80bcd'}
        flashcard = flashcard.Flashcard(**f)
        storage.add(flashcard)
        storage.save()

        p = {'flashcard_id': 'c19be55b-aa0e-40e1-b1de-f36cac5ce778', 'review_count': 10, 'correct_count': 5, 'last_review_date': datetime.now()}
        progress = progress.Progress(**p)
        storage.add(progress)
        storage.save()
