#!/usr/bin/python3
""" Decks API Endpoint """


from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models.deck import Deck
from app import db

decks_view = Blueprint('decks_view', __name__, url_prefix='/api/v1/')

@decks_view.route('/users/me/decks', methods=['GET'],
                  strict_slashes=False)
@login_required
def get_all_decks():
    """
    Retrieves all decks belonging to the current user.

    Returns:
    tuple: A tuple containing a JSON response with a list of decks and an HTTP status code 200.
    """
    decks_objs = db.session.query(Deck).filter_by(user_id=current_user.id).all()
    decks_list = [deck.to_dict() for deck in decks_objs]
    return jsonify(decks_list), 200
