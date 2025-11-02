/**
 * Review Session Controller
 * Orchestrates the flashcard review session
 */
class ReviewSession {
    /**
     * Create a new review session
     * @param {string} deckId - The deck ID
     * @param {Array} flashcards - Array of flashcard objects
     */
    constructor(deckId, flashcards) {
        this.manager = new FlashcardManager(deckId, flashcards);
        this.setupEventHandlers();
    }

    /**
     * Set up event handlers for user interactions
     */
    setupEventHandlers() {
        // Rating button handlers
        $(document).on('click', 'button.rating-button.again', () => {
            this.handleRating('again');
        });
        $(document).on('click', 'button.rating-button.hard', () => {
            this.handleRating('hard');
        });
        $(document).on('click', 'button.rating-button.good', () => {
            this.handleRating('good');
        });
        $(document).on('click', 'button.rating-button.easy', () => {
            this.handleRating('easy');
        });

        // Delete button handler
        $(document).on('click', 'button.delete', () => {
            this.handleDelete();
        });

        // Edit button handler
        $(document).on('click', 'button.edit', () => {
            this.handleEdit();
        });
    }

    /**
     * Start the review session
     */
    async start() {
        await this.showNextFlashcard();
    }

    /**
     * Show the next flashcard in the sequence
     */
    async showNextFlashcard() {
        // Check if we've reached the end of current cards
        if (this.manager.getCurrentFlashcard() === null) {
            const hasMoreCards = this.manager.handleEndOfDeck();
            if (!hasMoreCards) {
                UIManager.showCompletionMessage();
                return;
            }
        }

        const flashcard = this.manager.getCurrentFlashcard();
        
        // Check if this card should bypass date check (immediate review)
        if (this.manager.shouldBypassDateCheck()) {
            UIManager.showFlashcard(flashcard);
            return;
        }
        
        // Check if card is due for review
        try {
            const progress = await FlashcardAPI.getProgress(flashcard.id);
            
            if (this.manager.isCardDue(progress)) {
                UIManager.showFlashcard(flashcard);
            } else {
                if (CONFIG.DEBUG) {
                    const nextReviewDate = new Date(progress.next_review_date);
                    console.log(`Skipping card ${flashcard.id} - not due yet (due: ${nextReviewDate.toLocaleString()})`);
                }
                this.manager.moveToNext();
                await this.showNextFlashcard();
            }
        } catch (error) {
            console.error('Failed to fetch flashcard progress:', error);
            this.manager.moveToNext();
            await this.showNextFlashcard();
        }
    }

    /**
     * Handle rating button click
     * @param {string} rating - The rating ('again', 'hard', 'good', 'easy')
     */
    async handleRating(rating) {
        const flashcard = this.manager.getCurrentFlashcard();
        if (!flashcard) return;

        try {
            // Update progress on backend
            await this.updateProgress(flashcard.id, rating);
            
            // Handle failed cards (again/hard)
            if (rating === 'again' || rating === 'hard') {
                this.manager.markForImmediateReview();
            }
            
            // Move to next card
            this.manager.moveToNext();
            
            // Reset UI and show next card
            UIManager.resetFlashcardView();
            await this.showNextFlashcard();
            
        } catch (error) {
            console.error('Failed to handle rating:', error);
            UIManager.showError('Failed to save progress. Please try again.');
        }
    }

    /**
     * Update progress for a flashcard
     * @param {string} flashcardId - The flashcard ID
     * @param {string} rating - The rating
     */
    async updateProgress(flashcardId, rating) {
        try {
            // Get current progress
            const progress = await FlashcardAPI.getProgress(flashcardId);
            
            // Validate and apply SM2 algorithm
            const validatedProgress = validateProgress(progress);
            const updatedProgress = sm2Algorithm(validatedProgress, rating);
            
            // Display user feedback
            const nextReview = getNextReviewDescription(updatedProgress.next_review_date);
            const stats = calculateLearningStats(updatedProgress);
            
            if (CONFIG.DEBUG) {
                console.log(`Progress updated! Next review: ${nextReview}. Stats: ${stats.accuracy} accuracy, ${stats.reviews} reviews`);
            }

            // Save to backend
            await FlashcardAPI.updateProgress(flashcardId, updatedProgress);
            
        } catch (error) {
            console.error('Failed to update progress:', error);
            throw error;
        }
    }

    /**
     * Handle delete button click
     */
    async handleDelete() {
        if (!confirm('Are you sure you want to delete this flashcard?')) {
            return;
        }

        const flashcard = this.manager.getCurrentFlashcard();
        if (!flashcard) return;

        try {
            await FlashcardAPI.deleteFlashcard(flashcard.id);
            console.log(`Flashcard ${flashcard.id} deleted successfully`);
            
            // Remove card from manager (doesn't increment index)
            this.manager.removeCurrentFlashcard();
            
            // Reset UI to clear any stale data
            UIManager.resetFlashcardView();
            
            // Show next card
            await this.showNextFlashcard();
            
        } catch (error) {
            console.error('Failed to delete flashcard:', error);
            UIManager.showError('Failed to delete flashcard. Please try again.');
        }
    }

    /**
     * Handle edit button click
     */
    handleEdit() {
        const flashcard = this.manager.getCurrentFlashcard();
        if (!flashcard) return;
        
        window.location.href = `/users/me/flashcards/${flashcard.id}/edit`;
    }
}
