#!/usr/bin/python3
""" new_flashcard module """


from flask import (Flask, render_template, flash, Blueprint,
                   redirect, url_for, current_app as app)
from app.models.deck import Deck
from app.models.user import User
from app.models.flashcard import Flashcard
from flask_login import login_required


bp = Blueprint('flashcards', __name__)

@bp.route('/users/<user_id>/flashcards/new', methods=['GET', 'POST'],
          strict_slashes=False)
@login_required
def new_flashcard(user_id):
    """
    Displays the new flashcard page and adds the newly
    created flashcard to the database 
    """
    from app.forms.new_flashcard_form import NewFlashcardForm
    form = NewFlashcardForm()
    decks_list = Deck.query.filter_by(user_id=user_id).order_by(Deck.name)
    form.deck.choices = [(deck.id, deck.name) for deck in decks_list]
    form.deck.choices.append(('new', 'Add new Deck'))

    if form.validate_on_submit():
        selected_deck = form.deck.data
        if selected_deck == 'new':
            deck_id = ""
        else:
            deck_id = selected_deck

        question = form.front.data or ""
        answer = form.back.data or ""
        #create a new flashcard and save it to the database
        flashcard = Flashcard(question=question, answer=answer, deck_id=deck_id)
        flashcard.save()
        app.logger.info('new flashcard dict:' + str(flashcard.to_dict()))
        return redirect(url_for('flashcards.new_flashcard', user_id=user_id))

    else:
        flash('Some information is missing')
    
    return render_template('new_flashcard.html', form=form)



@bp.route('/users/<user_id>/decks/<deck_id>/flashcards/<flashcard_id>/edit', methods=['GET', 'POST', 'PUT'],
          strict_slashes=False)
@login_required
def edit_flashcard(user_id, deck_id, flashcard_id):
    """
    Displays the edit flashcard page and updates the flashcard
    in the database
    """
    from app.forms.edit_flashcard_form import EditFlashcardForm
    form = EditFlashcardForm()
    decks_list = Deck.query.filter_by(user_id=user_id).order_by(Deck.name)
    form.deck.choices = [(deck.id, deck.name) for deck in decks_list]
    form.deck.choices.append(('new', 'Add new Deck'))
    # setting the default of the deck select element to be the deck_id
    # of the flashcard the user wants to edit
    form.deck.default = deck_id
    form.process()

    flashcard = app.storage.get(Flashcard, flashcard_id)
    form.front.data = flashcard.question
    form.back.data = flashcard.answer
    
    if form.validate_on_submit():
        selected_deck = form.deck.data
        if selected_deck == 'new':
            deck_id = ""
        else:
            deck_id = selected_deck
            flashcard = app.storage.get(Flashcard, flashcard_id)
            flashcard.deck_id = deck_id
            flashcard.question = form.front.data or ""
            flashcard.answer = form.back.data or ""
            app.storage.save()
            # This line will be editted:
            return redirect(url_for('flashcards.edit_flashcard',
                            user_id=user_id, deck_id=deck_id, flashcard_id=flashcard_id))
    else:
        flash('Some information is missing')

    return render_template('edit_flashcard.html', form=form,
                           deck_id=deck_id, flashcard_id=flashcard_id)



@bp.route('/users/<user_id>/decks/<deck_id>/flashcards/<flashcard_id>',
           strict_slashes=False)
@login_required
def show_flashcard(user_id, deck_id, flashcard_id):
    """ Displays the flashcard page """
    deck = storage.get(Deck, deck_id)
    flashcard = app.storage.get(Flashcard, flashcard_id)

    return render_template('show_flashcard.html', deck=deck,
                           flashcard=flashcard)
