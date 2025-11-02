/**
 * Flashcard Manager
 * Manages flashcard review sessions including state, progression, and spaced repetition
 */
class FlashcardManager {
    /**
     * Create a new FlashcardManager instance
     * @param {string} deckId - The deck ID to manage
     * @param {Array} flashcards - Array of flashcard objects
     */
    constructor(deckId, flashcards) {
        this.deckId = deckId;
        this.flashcards = flashcards;
        this.currentIndex = 0;
        this.reviewAgainFlashcards = []; // Cards that need review at end of session
        this.immediateReviewCards = new Set(); // Cards marked for immediate review
    }

    /**
     * Get the current flashcard
     * @returns {Object|null} Current flashcard or null if none available
     */
    getCurrentFlashcard() {
        if (this.currentIndex >= this.flashcards.length) {
            return null;
        }
        return this.flashcards[this.currentIndex];
    }

    /**
     * Check if review session is complete
     * @returns {boolean} True if all cards have been reviewed
     */
    isSessionComplete() {
        return this.currentIndex >= this.flashcards.length && 
               this.immediateReviewCards.size === 0 && 
               this.reviewAgainFlashcards.length === 0;
    }

    /**
     * Check if current card is due for review
     * @param {Object} progress - Progress object for current card
     * @returns {boolean} True if card is due for review
     */
    isCardDue(progress) {
        const now = new Date();
        const nextReviewDate = new Date(progress.next_review_date);
        return nextReviewDate <= now;
    }

    /**
     * Mark current card for immediate review (failed/hard ratings)
     */
    markForImmediateReview() {
        const currentCard = this.getCurrentFlashcard();
        if (!currentCard) return;

        this.reviewAgainFlashcards.push(currentCard);
        this.immediateReviewCards.add(currentCard.id);
        
        if (CONFIG.DEBUG) {
            console.log(`Card ${currentCard.id} marked for immediate review at end of deck`);
            console.log(`Review queue size: ${this.reviewAgainFlashcards.length}`);
        }
    }

    /**
     * Move to next flashcard
     */
    moveToNext() {
        this.currentIndex++;
        if (CONFIG.DEBUG) {
            console.log(`Moving to card ${this.currentIndex}/${this.flashcards.length}`);
        }
    }

    /**
     * Handle end of deck - add failed cards back for review
     * @returns {boolean} True if cards were added, false if session is complete
     */
    handleEndOfDeck() {
        // First, check for immediate review cards
        if (this.immediateReviewCards.size > 0) {
            console.log(`All regular cards done. Now showing ${this.immediateReviewCards.size} immediate review cards.`);
            
            // Add immediate review cards back to the deck
            const immediateCards = this.reviewAgainFlashcards.filter(
                card => this.immediateReviewCards.has(card.id)
            );
            this.flashcards.push(...immediateCards);
            
            // Remove these cards from reviewAgainFlashcards
            this.reviewAgainFlashcards = this.reviewAgainFlashcards.filter(
                card => !this.immediateReviewCards.has(card.id)
            );
            
            this.currentIndex = 0;
            console.log(`Added ${immediateCards.length} immediate review cards to deck`);
            return true;
        } 
        
        // Then, check for remaining failed cards
        if (this.reviewAgainFlashcards.length > 0) {
            this.flashcards.push(...this.reviewAgainFlashcards);
            const addedCount = this.reviewAgainFlashcards.length;
            this.reviewAgainFlashcards = [];
            this.currentIndex = 0;
            console.log(`Added ${addedCount} failed cards back for review`);
            return true;
        }
        
        // Session is complete
        return false;
    }

    /**
     * Check if current card should bypass date check (immediate review)
     * @returns {boolean} True if card should be shown immediately
     */
    shouldBypassDateCheck() {
        const currentCard = this.getCurrentFlashcard();
        if (!currentCard) return false;
        
        const shouldBypass = this.immediateReviewCards.has(currentCard.id);
        if (shouldBypass) {
            console.log(`Showing immediate review card: ${currentCard.id}`);
            this.immediateReviewCards.delete(currentCard.id);
        }
        return shouldBypass;
    }

    /**
     * Get statistics about current session
     * @returns {Object} Session statistics
     */
    getStats() {
        return {
            current: this.currentIndex + 1,
            total: this.flashcards.length,
            reviewQueue: this.reviewAgainFlashcards.length,
            immediateReview: this.immediateReviewCards.size,
            remaining: this.flashcards.length - this.currentIndex
        };
    }
}
