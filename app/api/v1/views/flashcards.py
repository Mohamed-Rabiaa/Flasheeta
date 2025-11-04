#!/usr/bin/python3
""" Flashcards API Endpoints """

from flask import Blueprint, jsonify, current_app as app
from flask_login import login_required, current_user
from app.models.flashcard import Flashcard
from app.services.flashcard_service import FlashcardService
from app.exceptions import NotFoundError
from app import db, csrf

flashcards_view = Blueprint('flashcards_view', __name__, url_prefix='/api/v1/') 

@flashcards_view.route('/users/me/decks/<deck_id>/flashcards', methods=['GET'],
                       strict_slashes=False)
@csrf.exempt
@login_required
def get_all_flashcards(deck_id):
    """
    Retrieves all flashcards related to the chosen deck of the current user.

    Args:
        deck_id (str): The ID of the deck to retrieve flashcards from.

    Returns:
        tuple: A tuple containing a JSON response with a list of flashcards and an HTTP status code 200.
    """
    flashcards_objs = FlashcardService.get_flashcards_by_deck(deck_id)
    flashcards_list = [flashcard.to_dict() for flashcard in flashcards_objs]
    return jsonify(flashcards_list), 200


@flashcards_view.route('/users/me/flashcards/<flashcard_id>',
                       methods=['GET'], strict_slashes=False)
@csrf.exempt
@login_required
def get_flashcard(flashcard_id):
    """
    Retrieves a specific flashcard by its ID.

    Args:
        flashcard_id (str): The ID of the flashcard to retrieve.

    Returns:
        tuple: A tuple containing a JSON response with the flashcard data and an HTTP status code 200 if found,
               or raises NotFoundError if the flashcard is not found.
    """
    flashcard = FlashcardService.get_flashcard_by_id(flashcard_id)
    if not flashcard:
        raise NotFoundError('Flashcard not found')

    return jsonify(flashcard.to_dict()), 200


@flashcards_view.route('/users/me/flashcards/<flashcard_id>',
                       methods=['DELETE'], strict_slashes=False)
@login_required
def delete_flashcard(flashcard_id):
    """
    Deletes a specific flashcard by its ID.

    Args:
        flashcard_id (str): The ID of the flashcard to delete.

    Returns:
        tuple: Success message with HTTP status code 200 if deletion is successful,
               or raises NotFoundError if the flashcard is not found.
    """
    if not FlashcardService.delete_flashcard(flashcard_id):
        raise NotFoundError('Flashcard not found')

    return jsonify({'message': 'Flashcard deleted successfully'}), 200
