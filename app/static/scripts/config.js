/**
 * Configuration constants for Flasheeta application
 */
const CONFIG = {
    // API Configuration
    API: {
        BASE_URL: ['localhost', '127.0.0.1', '0.0.0.0'].includes(window.location.hostname)
            ? '' // Use relative URLs for local development
            : 'http://158.180.238.158:5000', // Production URL
    },

    // Spaced Repetition Intervals (in minutes)
    INTERVALS: {
        AGAIN: 10,  // 10 minutes for failed cards
        HARD: 15,   // 15 minutes for hard cards
    },

    // UI Messages
    MESSAGES: {
        NO_DECKS: "You don't have any decks yet. Go to the New Flashcard page and add a new deck.",
        DECK_COMPLETE: "Congratulations! You have finished all the flashcards in this deck.",
        NO_FLASHCARDS: "No flashcards found in this deck.",
    },

    // Debug mode
    DEBUG: ['localhost', '127.0.0.1'].includes(window.location.hostname),
};

// Log configuration in debug mode
if (CONFIG.DEBUG) {
    console.log('Flasheeta Config:', CONFIG);
}
