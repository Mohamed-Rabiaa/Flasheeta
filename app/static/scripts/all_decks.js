$(document).ready(async function() {
    try {
	//Getting all decks of the current user
        const deckData = await $.get('https://flasheeta.pythonanywhere.com/api/v1/users/me/decks');
	if (deckData.length === 0) {
	     	    $('div.parent').append('<p>You don\'t have any decks yet, Go to the New Flashcard page and add a new deck</p>');
	}
        for (let i = 0; i < deckData.length; i++) {
            const deckName = deckData[i]['name'];
            const deckId = deckData[i]['id'];
            const deck = $('<button class="deck"></button>').text(deckName);

            $('div.parent').append(deck);

            deck.on('click', async function() {
		//After clicking on the deck button we clear the decks and show the flashcards of the clicked deck
                $('div.parent').empty();
                $('body').append(flashcardHtml());

                const stylesheetUrl = $('#config').data('stylesheet-url');
                if (!$('link[href="' + stylesheetUrl + '"]').length) {
                    const link = $('<link rel="stylesheet" type="text/css" href="' + stylesheetUrl + '">');
                    $('head').append(link);
                }

                try {
                    const flashcards = await $.get(`https://flasheeta.pythonanywhere.com/api/v1/users/me/decks/${deckId}/flashcards`);
                    if (flashcards.length > 0) {
                        let currentFlashcardIndex = 0;
                        let reviewAgainFlashcards = [];

                        async function showNextFlashcard() {
                            if (currentFlashcardIndex >= flashcards.length) {
                                if (reviewAgainFlashcards.length > 0) {
                                    flashcards.push(...reviewAgainFlashcards);
                                    reviewAgainFlashcards = [];
                                    currentFlashcardIndex = 0;
                                } else {
                                    $('div.flashcard').remove();
                                    $('div.parent').append('<p>Congratulations, You have finished all the flashcards in this deck</p>');
                                    return;
                                }
                            }

                            const flashcard = flashcards[currentFlashcardIndex];
                            try {
                                const progress = await $.get(`https://flasheeta.pythonanywhere.com/api/v1/users/me/flashcards/${flashcard.id}/progress`);
                                const now = new Date();
                                const nextReviewDate = new Date(progress['next_review_date']);

                                if (nextReviewDate <= now) {
                                    showFlashcard(flashcard);
                                    return;
                                } else {
                                    currentFlashcardIndex++;
                                    await showNextFlashcard();
                                }
                            } catch (error) {
                                console.error('Failed to fetch flashcard progress:', error);
                                currentFlashcardIndex++;
                                await showNextFlashcard();
                            }
                        }

                        await showNextFlashcard();

                        async function handleRatingClick(rating) {
                            const flashcardId = flashcards[currentFlashcardIndex]['id'];
                            await updateProgress(flashcardId, rating);
                            if (rating === 'again' || rating === 'hard') {
                                reviewAgainFlashcards.push(flashcards[currentFlashcardIndex]);
				flashcards.splice(currentFlashcardIndex, 1);
				flashcards.push(flashcards[currentFlashcardIndex]);
                            } else {
				currentFlashcardIndex++;
			    }
                            await showNextFlashcard();
                            resetFlashcardView();
                        }

                        $(document).on('click', 'button.again', async function() {
                            await handleRatingClick('again');
                        });
                        $(document).on('click', 'button.hard', async function() {
                            await handleRatingClick('hard');
                        });
                        $(document).on('click', 'button.good', async function() {
                            await handleRatingClick('good');
                        });
                        $(document).on('click', 'button.easy', async function() {
                            await handleRatingClick('easy');
                        });

                        $(document).on('click', 'button.delete', function() {
			    if (confirm('Are you sure you want to delete this flashcard?')) {

				const flashcardId = flashcards[currentFlashcardIndex]['id'];
				$.ajax({
                                    url: `https://flasheeta.pythonanywhere.com/api/v1/users/me/flashcards/${flashcardId}`,
                                    type: 'DELETE',
                                    headers: {
					'X-CSRFToken': getCsrfToken()
                                    },
                                    success: function(response) {
					console.log(`Flashcard: ${flashcardId} deleted successfully:`, response);
					currentFlashcardIndex++;
					showNextFlashcard();
                                    },
                                    error: function(xhr, status, error) {
					console.error(`Flashcard: ${flashcardId} delete failed:`, error);
                                    }
				});
			    }
                        });

			$(document).on('click', 'button.edit', function() {
			    const flashcardId = flashcards[currentFlashcardIndex]['id'];
			    window.location.href = `/users/me/flashcards/${flashcardId}/edit`;
			});
                    } else {
                        console.error('No flashcards found');
                    }
                } catch (error) {
                    console.error('Failed to fetch flashcards:', error);
                }
            });
        }
    } catch (error) {
        console.error('Failed to fetch decks:', error);
    }
});

function flashcardHtml() {
    const html = "<div class='flashcard'> \
<div class='info'> \
<p class='question'></p> \
</div> \
<div class='actions'> \
<button class='edit'>Edit</button> \
<button class='show_answer'>Show Answer</button> \
<button class='delete'>Delete</button> \
</div> \
<div class='rating'> \
</div> \
</div>";
    return html;
}

function ratingButtonsHtml() {
    const html = '<button class="again">Again</button> \
<button class="hard">Hard</button> \
<button class="good">Good</button> \
<button class="easy">Easy</button> \
';
    return html;
}

function updateProgress(flashcardId, rating) {
    $.get(`https://flasheeta.pythonanywhere.com/api/v1/users/me/flashcards/${flashcardId}/progress`, function(progress, status) {
        if (status === 'success') {
            const updatedProgress = sm2Algorithm(progress, rating);

            $.ajax({
                url: `https://flasheeta.pythonanywhere.com/api/v1/users/me/flashcards/${flashcardId}/progress`,
                type: 'PUT',
                data: JSON.stringify(updatedProgress),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                headers: {
                    'X-CSRFToken': getCsrfToken()
                },
                success: function(response) {
                    console.log('Update successful:', response);
                },
                error: function(xhr, status, error) {
                    console.error('Update failed:', error);
                }
            });
        }
    });
}

//Spaced repetition algorithm
function sm2Algorithm(progress, rating) {
    let { review_count, correct_count, ease_factor, interval, last_review_date } = progress;

    last_review_date = new Date(last_review_date);

    const ratings = {
        again: 0,
        hard: 3,
        good: 4,
        easy: 5
    };

    const q = ratings[rating];

    if (q < 4) {
	if (q === 0) {
            interval = 1;
	}
	if (q === 3) {
	    interval = 2;
	}
    } else {
        if (review_count === 0) {
            interval = 1;
        } else if (review_count === 1) {
            interval = 6;
        } else {
	    if (q === 4) {
                interval *= 1.2;
	    }
	    else {
		interval *= ease_factor;
	    }
        }

        ease_factor = ease_factor + 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02);

        if (ease_factor < 1.3) {
            ease_factor = 1.3;
        }
    }

    review_count++;
    if (q > 2) {
        correct_count++;
    }

    let next_review_date = new Date(last_review_date);
    if (q <= 3) {
	next_review_date.setMinutes(next_review_date.getMinutes() + interval); // Add interval in minutes
    }
    else {
	next_review_date.setDate(next_review_date.getDate() + interval); // Add interval in days
    }
    console.log(next_review_date);

    return {
        review_count,
        correct_count,
        ease_factor,
        interval,
        next_review_date
    };
}

function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function showFlashcard(flashcard) {
    $('p.question').text(flashcard['question']);

    $('button.show_answer').one('click', function() {
        $('p.question').css('border-bottom', '3px solid');
        $('div.info').append('<p class="answer"></p>');
        $('p.answer').text(flashcard['answer']);

        if (!$('div.flashcard').has('div.rating').length) {
            $('div.flashcard').append('<div class="rating"></div>');
        }
        if ($('div.rating').children().length === 0) {
            $('div.rating').append(ratingButtonsHtml());
        }
    });
}

function resetFlashcardView() {
    $('p.question').css('border-bottom', '');
    $('p.answer').remove();
    $('div.rating').remove();
}
