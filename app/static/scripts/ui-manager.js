/**
 * UI Manager for Flashcard Display
 * Handles DOM manipulation and user interactions
 */
class UIManager {
    /**
     * Show empty state message
     * @param {string} message - Message to display
     */
    static showEmptyState(message) {
        $('div.decks-container').append(
            `<div class="empty-state"><p>${message}</p></div>`
        );
    }

    /**
     * Render a deck button
     * @param {Object} deck - Deck object with id and name
     * @param {Function} onClick - Click handler function
     */
    static renderDeck(deck, onClick) {
        const deckButton = $('<button class="deck-card"></button>').text(deck.name);
        $('div.decks-container').append(deckButton);
        deckButton.on('click', onClick);
    }

    /**
     * Clear the decks container and show flashcard container
     */
    static initFlashcardView() {
        $('div.decks-container').empty();
        $('body').append(this.getFlashcardHtml());
    }

    /**
     * Get HTML template for flashcard container
     * @returns {string} HTML string
     */
    static getFlashcardHtml() {
        return `
            <div class='flashcard-container'>
                <div class='flashcard-content'>
                    <p class='flashcard-question'></p>
                </div>
                <div class='flashcard-actions'>
                    <button class='flashcard-button edit'>Edit</button>
                    <button class='flashcard-button show-answer'>Show Answer</button>
                    <button class='flashcard-button delete'>Delete</button>
                </div>
                <div class='rating-container'></div>
            </div>
        `;
    }

    /**
     * Get HTML template for rating buttons
     * @returns {string} HTML string
     */
    static getRatingButtonsHtml() {
        return `
            <button class="rating-button again">Again</button>
            <button class="rating-button hard">Hard</button>
            <button class="rating-button good">Good</button>
            <button class="rating-button easy">Easy</button>
        `;
    }

    /**
     * Display a flashcard
     * @param {Object} flashcard - Flashcard object with question and answer
     */
    static showFlashcard(flashcard) {
        $('p.flashcard-question').text(flashcard.question);

        // Set up show answer button (one-time click)
        $('button.show-answer').one('click', function() {
            UIManager.showAnswer(flashcard.answer);
        });
    }

    /**
     * Show the answer and rating buttons
     * @param {string} answer - The answer text
     */
    static showAnswer(answer) {
        $('p.flashcard-question').css('border-bottom', '3px solid');
        $('div.flashcard-content').append('<p class="flashcard-answer"></p>');
        $('p.flashcard-answer').text(answer);

        // Add rating container if it doesn't exist
        if (!$('div.flashcard-container').has('div.rating-container').length) {
            $('div.flashcard-container').append('<div class="rating-container"></div>');
        }
        
        // Add rating buttons if they don't exist
        if ($('div.rating-container').children().length === 0) {
            $('div.rating-container').append(UIManager.getRatingButtonsHtml());
        }
    }

    /**
     * Reset flashcard view for next card
     */
    static resetFlashcardView() {
        $('p.flashcard-question').css('border-bottom', '').text('');
        $('p.flashcard-answer').remove();
        $('div.rating-container').remove();
        
        // Re-enable the show-answer button (remove any existing handlers)
        $('button.show-answer').off('click');
    }

    /**
     * Show completion message
     */
    static showCompletionMessage() {
        $('div.flashcard-container').remove();
        $('div.decks-container').append(
            `<div class="empty-state"><p>${CONFIG.MESSAGES.DECK_COMPLETE}</p></div>`
        );
    }

    /**
     * Show loading indicator (optional)
     */
    static showLoading() {
        $('div.decks-container').append('<div class="loading">Loading...</div>');
    }

    /**
     * Hide loading indicator (optional)
     */
    static hideLoading() {
        $('div.loading').remove();
    }

    /**
     * Show error message
     * @param {string} message - Error message to display
     */
    static showError(message) {
        console.error(message);
        // Could add visual error notification here
    }
}
