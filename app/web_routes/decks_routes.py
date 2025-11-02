#!/usr/bin/python3
"""
Routes for handling user decks in Flasheeta.
"""

from flask import current_app as app, render_template, Blueprint
from flask_login import login_required, current_user
from app.models.deck import Deck
from app.models.user import User
from app.services.deck_service import DeckService

bp = Blueprint('decks', __name__)

@bp.route('/users/me/decks', strict_slashes=False)
@login_required
def decks():
    """
    Displays all decks of the current logged-in user.

    Returns:
        render_template: Renders 'all_decks.html' template with the 'user' object.
    """
    # user = app.storage.get(User, current_user.id)
    return render_template('all_decks.html')
