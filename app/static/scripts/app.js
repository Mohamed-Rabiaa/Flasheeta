/**
 * Main Application Entry Point
 * Initializes the Flasheeta deck view and review system
 */

$(document).ready(async function() {
    // Configure jQuery to send cookies with AJAX requests
    $.ajaxSetup({
        xhrFields: {
            withCredentials: true
        }
    });
    
    try {
        // Fetch all decks for the current user
        const decks = await FlashcardAPI.getDecks();
        
        // Show empty state if no decks exist
        if (decks.length === 0) {
            UIManager.showEmptyState(CONFIG.MESSAGES.NO_DECKS);
            return;
        }
        
        // Render each deck
        decks.forEach(deck => {
            UIManager.renderDeck(deck, async () => {
                await startReviewSession(deck.id);
            });
        });
        
    } catch (error) {
        console.error('Failed to initialize application:', error);
        UIManager.showError('Failed to load decks. Please refresh the page.');
    }
});

/**
 * Start a review session for a specific deck
 * @param {string} deckId - The deck ID to review
 */
async function startReviewSession(deckId) {
    try {
        // Initialize the flashcard view
        UIManager.initFlashcardView();
        
        // Fetch flashcards for the selected deck
        const flashcards = await FlashcardAPI.getFlashcards(deckId);
        
        // Check if deck has flashcards
        if (flashcards.length === 0) {
            UIManager.showError(CONFIG.MESSAGES.NO_FLASHCARDS);
            return;
        }
        
        // Create and start the review session
        const session = new ReviewSession(deckId, flashcards);
        await session.start();
        
    } catch (error) {
        console.error('Failed to start review session:', error);
        UIManager.showError('Failed to load flashcards. Please try again.');
    }
}
