#!/usr/bin/python3
""" new_flashcard module """


from flask import (Flask, render_template, flash, Blueprint,
                   request, redirect, url_for, current_app as app)
from app.models.deck import Deck
from app.models.user import User
from app.models.flashcard import Flashcard
from app.models.progress import Progress
from flask_login import login_required, current_user
from datetime import datetime

bp = Blueprint('flashcards', __name__)

@bp.route('/users/me/flashcards/new', methods=['GET', 'POST'],
          strict_slashes=False)
@login_required
def new_flashcard():
    """
    Displays the new flashcard page and adds the newly
    created flashcard to the database 
    """
    from app.forms.new_flashcard_form import NewFlashcardForm
    form = NewFlashcardForm()
    decks_list = Deck.query.filter_by(user_id=current_user.id).order_by(Deck.name)
    form.deck.choices = [(deck.id, deck.name) for deck in decks_list]
    form.deck.choices.append(('new', 'Add new Deck'))

    if form.validate_on_submit():
        selected_deck = form.deck.data
        if selected_deck == 'new':
            deck_name = request.form.get('new_deck_name')
            if deck_name:
                new_deck = Deck(name=deck_name, user_id=current_user.id)
                new_deck.save()
                deck_id = new_deck.id
            else:
                flash('New deck name is required')
                return redirect(url_for('flashcards.new_flashcard'))  
        else:
            deck_id = selected_deck

        question = form.front.data or ""
        answer = form.back.data or ""
        #create a new flashcard and save it to the database
        flashcard = Flashcard(question=question, answer=answer, deck_id=deck_id)
        flashcard.save()
        
        #create a new progress with the flashcard_id and save it to the database
        progress = Progress(review_count=0, correct_count=0,
                            flashcard_id=flashcard.id, last_review_date=datetime.utcnow())
        progress.save()
        return redirect(url_for('flashcards.new_flashcard'))

    else:
        flash('Some information is missing')
    
    return render_template('new_flashcard.html', form=form)



@bp.route('/users/me/flashcards/<flashcard_id>/edit', methods=['GET', 'POST', 'PUT'],
          strict_slashes=False)
@login_required
def edit_flashcard(flashcard_id):
    """
    Displays the edit flashcard page and updates the flashcard
    in the database
    """
    from app.forms.edit_flashcard_form import EditFlashcardForm
    form = EditFlashcardForm()
    decks_list = Deck.query.filter_by(user_id=current_user.id).order_by(Deck.name)
    form.deck.choices = [(deck.id, deck.name) for deck in decks_list]
    form.deck.choices.append(('new', 'Add new Deck'))
    
    flashcard = app.storage.get(Flashcard, flashcard_id)
    if request.method == 'GET':
        # setting the default of the deck select element to be the deck_id
        # of the flashcard the user wants to edit
        form.deck.default = flashcard.deck_id
        form.process()
        form.front.data = flashcard.question
        form.back.data = flashcard.answer
    else:
        # Process form submission
        form.process(request.form)

    if form.validate_on_submit():
        selected_deck = form.deck.data
        if selected_deck == 'new':
            deck_name = request.form.get('new_deck_name')
            app.logger.info(deck_name)
            if deck_name:
                new_deck = Deck(name=deck_name, user_id=current_user.id)
                new_deck.save()
                deck_id = new_deck.id
                app.logger.info('Newly created deck: name={}, id={}, user_id={}'.format(
                    new_deck.name, new_deck.id, new_deck.user_id))
            else:
                flash('New deck name is required')
                return redirect(url_for('flashcards.new_flashcard'))
        else:
            # Process form submission
            form.process(request.form)
            deck_id = selected_deck
          
        flashcard.question = form.front.data or ""
        flashcard.answer = form.back.data or ""
        flashcard.deck_id = deck_id
        app.logger.info('Updated flashcard data: question={}, answer={}, deck_id={}'.format(
            flashcard.question, flashcard.answer, flashcard.deck_id))
        flashcard.save()

        return redirect(url_for('decks.decks'))
    else:
        flash('Some information is missing')

    return render_template('edit_flashcard.html', form=form, flashcard_id=flashcard_id)


@bp.route('/users/me/decks/<deck_name>/flashcards',
           strict_slashes=False)
@login_required
def show_flashcards(deck_name):
    """ Displays the show flashcards page """
    return render_template('show_flashcards.html')
