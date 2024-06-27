#!/usr/bin/python3
""" """


from flask import current_app as app, Flask, render_template, Blueprint
from flask_login import login_required
from app.models.deck import Deck
from app.models.user import User

bp = Blueprint('decks', __name__)

@bp.route('/users/<user_id>/decks', strict_slashes=False)
@login_required
def decks(user_id):
    """ Displays all decks of a given user """
    user = app.storage.get(User, user_id)
    return render_template('all_decks.html', user=user)
