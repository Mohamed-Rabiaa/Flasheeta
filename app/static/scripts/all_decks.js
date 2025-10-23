// Use relative URLs to avoid cross-origin issues
const API_BASE_URL = 
    ['localhost', '127.0.0.1', '0.0.0.0'].includes(window.location.hostname)
        ? '' // Use relative URLs for local development
        : 'http://158.180.238.158:5000'; // oracle cloud instance public ip address

console.log(API_BASE_URL);

$(document).ready(async function() {
    // Configure jQuery to send cookies with AJAX requests
    $.ajaxSetup({
        xhrFields: {
            withCredentials: true
        }
    });
    
    try {
	//Getting all decks of the current user
        const deckData = await $.get(`${API_BASE_URL}/api/v1/users/me/decks`);
        console.log("length of deckData: ", deckData.length);
	if (deckData.length === 0) {
	     	    $('div.decks-container').append('<div class="empty-state"><p>You don\'t have any decks yet. Go to the New Flashcard page and add a new deck.</p></div>');
	}
        for (let i = 0; i < deckData.length; i++) {
            const deckName = deckData[i]['name'];
            const deckId = deckData[i]['id'];
            const deck = $('<button class="deck-card"></button>').text(deckName);

            $('div.decks-container').append(deck);

            deck.on('click', async function() {
                // After clicking on the deck button we clear the decks and show the flashcards of the clicked deck
                $('div.decks-container').empty();
                $('body').append(flashcardHtml());

                try {
                    const flashcards = await $.get(`${API_BASE_URL}/api/v1/users/me/decks/${deckId}/flashcards`);
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
                                    $('div.flashcard-container').remove();
                                    $('div.decks-container').append('<div class="empty-state"><p>Congratulations! You have finished all the flashcards in this deck.</p></div>');
                                    return;
                                }
                            }

                            const flashcard = flashcards[currentFlashcardIndex];
                            try {
                                const progress = await $.get(`${API_BASE_URL}/api/v1/users/me/flashcards/${flashcard.id}/progress`);
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

                        $(document).on('click', 'button.rating-button.again', async function() {
                            await handleRatingClick('again');
                        });
                        $(document).on('click', 'button.rating-button.hard', async function() {
                            await handleRatingClick('hard');
                        });
                        $(document).on('click', 'button.rating-button.good', async function() {
                            await handleRatingClick('good');
                        });
                        $(document).on('click', 'button.rating-button.easy', async function() {
                            await handleRatingClick('easy');
                        });

                        $(document).on('click', 'button.delete', function() {
			    if (confirm('Are you sure you want to delete this flashcard?')) {

				const flashcardId = flashcards[currentFlashcardIndex]['id'];
				$.ajax({
                                    url: `${API_BASE_URL}/api/v1/users/me/flashcards/${flashcardId}`,
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
    const html = "<div class='flashcard-container'> \
<div class='flashcard-content'> \
<p class='flashcard-question'></p> \
</div> \
<div class='flashcard-actions'> \
<button class='flashcard-button edit'>Edit</button> \
<button class='flashcard-button show-answer'>Show Answer</button> \
<button class='flashcard-button delete'>Delete</button> \
</div> \
<div class='rating-container'> \
</div> \
</div>";
    return html;
}

function ratingButtonsHtml() {
    const html = '<button class="rating-button again">Again</button> \
<button class="rating-button hard">Hard</button> \
<button class="rating-button good">Good</button> \
<button class="rating-button easy">Easy</button> \
';
    return html;
}

function updateProgress(flashcardId, rating) {
    $.get(`${API_BASE_URL}/api/v1/users/me/flashcards/${flashcardId}/progress`, function(progress, status) {
        if (status === 'success') {
            // Validate and ensure progress has all required fields
            const validatedProgress = validateProgress(progress);
            
            // Apply improved SM2 algorithm
            const updatedProgress = sm2Algorithm(validatedProgress, rating);
            
            // Display user feedback
            const nextReview = getNextReviewDescription(updatedProgress.next_review_date);
            const stats = calculateLearningStats(updatedProgress);
            console.log(`Progress updated! Next review: ${nextReview}. Stats: ${stats.accuracy} accuracy, ${stats.reviews} reviews`);

            $.ajax({
                url: `${API_BASE_URL}/api/v1/users/me/flashcards/${flashcardId}/progress`,
                type: 'PUT',
                data: JSON.stringify(updatedProgress),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                headers: {
                    'X-CSRFToken': getCsrfToken()
                },
                success: function(response) {
                    console.log('Update successful:', response);
                    // Could add UI feedback here showing the next review time
                },
                error: function(xhr, status, error) {
                    console.error('Update failed:', error);
                    console.error('Response:', xhr.responseText);
                }
            });
        }
    }).fail(function(xhr, status, error) {
        console.error('Failed to get current progress:', error);
    });
}

function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function showFlashcard(flashcard) {
    $('p.flashcard-question').text(flashcard['question']);

    $('button.show-answer').one('click', function() {
        $('p.flashcard-question').css('border-bottom', '3px solid');
        $('div.flashcard-content').append('<p class="flashcard-answer"></p>');
        $('p.flashcard-answer').text(flashcard['answer']);

        if (!$('div.flashcard-container').has('div.rating-container').length) {
            $('div.flashcard-container').append('<div class="rating-container"></div>');
        }
        if ($('div.rating-container').children().length === 0) {
            $('div.rating-container').append(ratingButtonsHtml());
        }
    });
}

function resetFlashcardView() {
    $('p.flashcard-question').css('border-bottom', '');
    $('p.flashcard-answer').remove();
    $('div.rating-container').remove();
}
