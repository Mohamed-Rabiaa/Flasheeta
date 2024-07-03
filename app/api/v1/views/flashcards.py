#!/usr/bin/python3
""" Flashcards """


from flask import (Blueprint, jsonify, abort, current_app as app)
from flask_login import login_required, current_user
from app.models.flashcard import Flashcard
from app import db

flashcards_view = Blueprint('flashcards_view', __name__, url_prefix='/api/v1/') 

@flashcards_view.route('/users/me/decks/<deck_id>/flashcards', methods=['GET'],
                  strict_slashes=False)
@login_required
def get_all_flashcards(deck_id):
    """
    Retrieves all the flashcards related to the choosed deck of the current user
    """
    flashcards_objs = db.session.query(Flashcard).filter_by(deck_id=deck_id).all()
    flashcards_list = [flashcard.to_dict() for flashcard in flashcards_objs]
    return jsonify(flashcards_list), 200


@flashcards_view.route('/users/me/flashcards/<flashcard_id>',
                       methods=['GET'], strict_slashes=False)
@login_required
def get_flashcard(flashcard_id):
    """
    Retrieves a flashcard by its id
    """
    flashcard = app.storage.get(Flashcard, flashcard_id)
    if not flashcard:
        return jsonify({'error': 'Not Found'}), 404

    return jsonify(flashcard.to_dict()), 200

@flashcards_view.route('/users/me/flashcards/<flashcard_id>',
                       methods=['DELETE'], strict_slashes=False)
@login_required
def delete_flashcard(flashcard_id):
    """
    Deletes a flashcard by its id
    """
    flashcard = app.storage.get(Flashcard, flashcard_id)
    if not flashcard:
        return jsonify({'error': 'Not Found'}), 404

    app.storage.delete(flashcard)
    app.storage.save()
    return jsonify({}), 204
