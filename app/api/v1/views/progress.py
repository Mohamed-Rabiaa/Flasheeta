#!/usr/bin/python3
""" Progress """


from flask import (Blueprint, jsonify, request, current_app as app)
from flask_login import login_required, current_user
from app.models.progress import Progress
from app import db

progress_view = Blueprint('progress_view', __name__, url_prefix='/api/v1/') 

@progress_view.route('/users/me/decks/<deck_id>/flashcards/<flashcard_id>/progress', methods=['GET'],
                  strict_slashes=False)
@login_required
def get_flashcard_progress(deck_id, flashcard_id):
    """
    Retrieves the progress of the flashcard with the flashcard_id
    """
    progress = db.session.query(Progress).filter_by(flashcard_id=flashcard_id).first()

    if not progress:
        return jsonify({'error': 'Not Found'}), 404

    return jsonify(progress.to_dict()), 200


@progress_view.route('/users/me/decks/<deck_id>/flashcards/<flashcard_id>/progress', methods=['PUT'],
                  strict_slashes=False)
@login_required
def update_flashcard_progress(deck_id, flashcard_id):
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
        setattr(progress, key, value)

    from datetime import datetime   
    setattr(progress, "updated_at", datetime.utcnow())
    setattr(progress, "last_review_date", datetime.utcnow())
    
