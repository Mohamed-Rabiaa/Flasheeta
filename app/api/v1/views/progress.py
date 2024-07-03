#!/usr/bin/python3
""" Progress """


from flask import (Blueprint, jsonify, request, current_app as app)
from flask_login import login_required, current_user
from app.models.progress import Progress
from app.models.flashcard import Flashcard
from app import db
from datetime import datetime


progress_view = Blueprint('progress_view', __name__, url_prefix='/api/v1/') 


@progress_view.route('/users/me/decks/<deck_id>/flashcards/progress', methods=['GET'],
                  strict_slashes=False)
@login_required
def get_flashcards_progress(deck_id):
    """
    Retrieves the progress of all flashcards in a specific deck
    """
    flashcards = db.session.query(Flashcard).filter_by(deck_id=deck_id).all()

    lst = []
    for flashcard in flashcards:
        progress = db.session.query(Progress).filter_by(flashcard_id=flashcard.id).first()
        if progress:
            lst.append(progress.to_dict())


@progress_view.route('/users/me/flashcards/<flashcard_id>/progress', methods=['GET'],
                  strict_slashes=False)
@login_required
def get_flashcard_progress(flashcard_id):
    """
    Retrieves the progress of the flashcard with the flashcard_id
    """
    progress = db.session.query(Progress).filter_by(flashcard_id=flashcard_id).first()

    if not progress:
        return jsonify({'error': 'Not Found'}), 404

    return jsonify(progress.to_dict()), 200


@progress_view.route('/users/me/flashcards/<flashcard_id>/progress', methods=['PUT'],
                  strict_slashes=False)
@login_required
def update_flashcard_progress(flashcard_id):
    """
    Updates the the progress of the flashcard with the flashcard_id
    """
    progress = db.session.query(Progress).filter_by(flashcard_id=flashcard_id).first()
    if not progress:
        return jsonify({'error': 'Not Found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    for key, value in data.items():
        if key == 'next_review_date':
            try:
                # Convert the datetime string to a MySQL Datetime format
                value = datetime.fromisoformat(value.replace('Z', '+00:00'))
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                return jsonify({'error': 'Invalid datetime format'}), 400
        setattr(progress, key, value)
 
    setattr(progress, "updated_at", datetime.utcnow())
    setattr(progress, "last_review_date", datetime.utcnow())
    progress.save()

    return jsonify(progress.to_dict()), 200

