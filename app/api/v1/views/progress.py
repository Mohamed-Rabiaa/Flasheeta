#!/usr/bin/python3
""" Progress API Endpoints """

from flask import Blueprint, jsonify, request, current_app as app
from flask_login import login_required
from app.models.progress import Progress
from app.models.flashcard import Flashcard
from app.services.progress_service import ProgressService
from app.services.flashcard_service import FlashcardService
from app import db, csrf
from datetime import datetime

progress_view = Blueprint('progress_view', __name__, url_prefix='/api/v1/') 

@progress_view.route('/users/me/decks/<deck_id>/flashcards/progress', methods=['GET'],
                     strict_slashes=False)
@csrf.exempt
@login_required
def get_flashcards_progress(deck_id):
    """
    Retrieves the progress of all flashcards in a specific deck.

    Args:
        deck_id (str): The ID of the deck for which progress is retrieved.

    Returns:
        tuple: A tuple containing a JSON response with the progress of flashcards in the deck
               and an HTTP status code 200.
    """
    flashcards = FlashcardService.get_flashcards_by_deck(deck_id)
    progress_list = []
    for flashcard in flashcards:
        progress = ProgressService.get_progress(flashcard.id)
        if progress:
            progress_list.append(progress.to_dict())
    
    return jsonify(progress_list), 200


@progress_view.route('/users/me/flashcards/<flashcard_id>/progress', methods=['GET'],
                     strict_slashes=False)
@csrf.exempt
@login_required
def get_flashcard_progress(flashcard_id):
    """
    Retrieves the progress of a specific flashcard.

    Args:
        flashcard_id (str): The ID of the flashcard for which progress is retrieved.

    Returns:
        tuple: A tuple containing a JSON response with the progress of the flashcard
               and an HTTP status code 200 if found, or a JSON response with an error
               message and HTTP status code 404 if not found.
    """
    progress = ProgressService.get_progress(flashcard_id)

    if not progress:
        return jsonify({'error': 'Not Found'}), 404

    return jsonify(progress.to_dict()), 200


@progress_view.route('/users/me/flashcards/<flashcard_id>/progress', methods=['PUT'],
                     strict_slashes=False)
@login_required
def update_flashcard_progress(flashcard_id):
    """
    Updates the progress of a specific flashcard.

    Args:
        flashcard_id (str): The ID of the flashcard for which progress is updated.

    Returns:
        tuple: A tuple containing a JSON response with the updated progress of the flashcard
               and an HTTP status code 200 if successful, or a JSON response with an error
               message and HTTP status code 404 if the flashcard is not found, or a JSON
               response with an error message and HTTP status code 400 if the request body
               is not valid JSON or if the datetime format is invalid.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    # Validate datetime format if present
    if 'next_review_date' in data:
        try:
            datetime.fromisoformat(data['next_review_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid datetime format'}), 400

    # Update progress using service
    progress = ProgressService.update_progress(flashcard_id, data)
    if not progress:
        return jsonify({'error': 'Not Found'}), 404

    return jsonify(progress.to_dict()), 200
