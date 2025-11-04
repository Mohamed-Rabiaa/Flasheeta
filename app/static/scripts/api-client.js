/**
 * API Client for Flasheeta
 * Handles all HTTP requests to the backend API
 */
class FlashcardAPI {
    /**
     * Get CSRF token from meta tag
     * @returns {string} CSRF token
     */
    static getCsrfToken() {
        return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
    }

    /**
     * Get all decks for current user
     * @returns {Promise<Array>} Array of deck objects
     */
    static async getDecks() {
        try {
            const response = await $.get(`${CONFIG.API.BASE_URL}/api/v1/users/me/decks`);
            if (CONFIG.DEBUG) {
                console.log('Fetched decks:', response.length);
            }
            return response;
        } catch (error) {
            console.error('Failed to fetch decks:', error);
            throw error;
        }
    }

    /**
     * Get all flashcards for a specific deck
     * @param {string} deckId - The deck ID
     * @returns {Promise<Array>} Array of flashcard objects
     */
    static async getFlashcards(deckId) {
        try {
            const response = await $.get(
                `${CONFIG.API.BASE_URL}/api/v1/users/me/decks/${deckId}/flashcards`
            );
            if (CONFIG.DEBUG) {
                console.log(`Fetched ${response.length} flashcards for deck ${deckId}`);
            }
            return response;
        } catch (error) {
            console.error(`Failed to fetch flashcards for deck ${deckId}:`, error);
            throw error;
        }
    }

    /**
     * Get progress for a specific flashcard
     * @param {string} flashcardId - The flashcard ID
     * @returns {Promise<Object>} Progress object
     */
    static async getProgress(flashcardId) {
        try {
            return await $.get(
                `${CONFIG.API.BASE_URL}/api/v1/users/me/flashcards/${flashcardId}/progress`
            );
        } catch (error) {
            console.error(`Failed to fetch progress for flashcard ${flashcardId}:`, error);
            throw error;
        }
    }

    /**
     * Update progress for a specific flashcard
     * @param {string} flashcardId - The flashcard ID
     * @param {Object} progressData - Updated progress data
     * @returns {Promise<Object>} Updated progress object
     */
    static async updateProgress(flashcardId, progressData) {
        try {
            const response = await $.ajax({
                url: `${CONFIG.API.BASE_URL}/api/v1/users/me/flashcards/${flashcardId}/progress`,
                type: 'PUT',
                data: JSON.stringify(progressData),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                }
            });
            if (CONFIG.DEBUG) {
                console.log('Progress updated successfully:', response);
            }
            return response;
        } catch (error) {
            console.error(`Failed to update progress for flashcard ${flashcardId}:`, error);
            throw error;
        }
    }

    /**
     * Delete a flashcard
     * @param {string} flashcardId - The flashcard ID
     * @returns {Promise<void>}
     */
    static async deleteFlashcard(flashcardId) {
        try {
            await $.ajax({
                url: `${CONFIG.API.BASE_URL}/api/v1/users/me/flashcards/${flashcardId}`,
                type: 'DELETE',
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                }
            });
            if (CONFIG.DEBUG) {
                console.log(`Flashcard ${flashcardId} deleted successfully`);
            }
        } catch (error) {
            console.error(`Failed to delete flashcard ${flashcardId}:`, error);
            // Log more details about the error
            if (error.responseJSON) {
                console.error('Error response:', error.responseJSON);
            } else if (error.responseText) {
                console.error('Error text:', error.responseText);
            }
            console.error('Status:', error.status, 'Status Text:', error.statusText);
            throw error;
        }
    }
}
