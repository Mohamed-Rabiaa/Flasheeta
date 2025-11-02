#!/usr/bin/python3
"""
Routes for managing flashcards in Flasheeta.
"""

from flask import (
    Flask, render_template, flash, Blueprint, request, redirect, url_for, current_app as app
)
from app.models.deck import Deck
from app.models.user import User
from app.models.flashcard import Flashcard
from app.models.progress import Progress
from app.services.flashcard_service import FlashcardService
from app.services.deck_service import DeckService
from flask_login import login_required, current_user
from datetime import datetime

bp = Blueprint('flashcards', __name__)

@bp.route('/users/me/flashcards/new', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def new_flashcard():
    """
    Displays the new flashcard page and adds the newly created flashcard to the database.
    If a new deck is added, it creates the deck and assigns the flashcard to it.

    Returns:
        render_template: Renders 'new_flashcard.html' template with the NewFlashcardForm object.
    """
    from app.forms.new_flashcard_form import NewFlashcardForm
    form = NewFlashcardForm()
    decks_list = DeckService.get_decks_by_user(current_user.id)
    form.deck.choices = [(deck.id, deck.name) for deck in decks_list]
    form.deck.choices.append(('new', 'Add new Deck'))

    if form.validate_on_submit():
        selected_deck = form.deck.data
        if selected_deck == 'new':
            deck_name = request.form.get('new_deck_name')
            if deck_name:
                try:
                    new_deck = DeckService.create_deck(deck_name, current_user.id)
                    deck_id = new_deck.id
                except ValueError as e:
                    flash(str(e))
                    return redirect(url_for('flashcards.new_flashcard'))
            else:
                flash('New deck name is required')
                return redirect(url_for('flashcards.new_flashcard'))
        else:
            deck_id = selected_deck

        question = form.front.data or ""
        answer = form.back.data or ""

        try:
            FlashcardService.create_flashcard(question, answer, deck_id)
            flash('New flashcard added successfully!')
        except ValueError as e:
            flash(str(e))
        
        return redirect(url_for('flashcards.new_flashcard'))

    return render_template('new_flashcard.html', form=form)


@bp.route('/users/me/flashcards/<flashcard_id>/edit', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def edit_flashcard(flashcard_id):
    """
    Displays the edit flashcard page and updates the flashcard in the database.
    Allows the user to change the deck of the flashcard or edit its content.

    Args:
        flashcard_id (str): The ID of the flashcard to edit.

    Returns:
        render_template: Renders 'edit_flashcard.html' template with the EditFlashcardForm object and flashcard_id.
    """
    from app.forms.edit_flashcard_form import EditFlashcardForm
    form = EditFlashcardForm()
    decks_list = DeckService.get_decks_by_user(current_user.id)
    form.deck.choices = [(deck.id, deck.name) for deck in decks_list]
    form.deck.choices.append(('new', 'Add new Deck'))

    flashcard = FlashcardService.get_flashcard_by_id(flashcard_id)
    if not flashcard:
        flash('Flashcard not found')
        return redirect(url_for('decks.decks'))

    if request.method == 'GET':
        form.deck.default = flashcard.deck_id
        form.process()
        form.front.data = flashcard.question
        form.back.data = flashcard.answer
    else:
        form.process(request.form)

    if form.validate_on_submit():
        selected_deck = form.deck.data
        if selected_deck == 'new':
            deck_name = request.form.get('new_deck_name')
            if deck_name:
                try:
                    new_deck = DeckService.create_deck(deck_name, current_user.id)
                    deck_id = new_deck.id
                except ValueError as e:
                    flash(str(e))
                    return redirect(url_for('flashcards.new_flashcard'))
            else:
                flash('New deck name is required')
                return redirect(url_for('flashcards.new_flashcard'))
        else:
            deck_id = selected_deck

        try:
            FlashcardService.update_flashcard(
                flashcard_id,
                form.front.data or "",
                form.back.data or "",
                deck_id
            )
            flash('Flashcard updated successfully!')
        except ValueError as e:
            flash(str(e))
        
        return redirect(url_for('decks.decks'))

    return render_template('edit_flashcard.html', form=form, flashcard_id=flashcard_id)

