import api from './api';

const progressService = {
  // Get progress for all flashcards in a deck
  getDeckProgress: async (deckId) => {
    const response = await api.get(`/users/me/decks/${deckId}/flashcards/progress`);
    return response.data;
  },

  // Get progress for single flashcard
  getProgress: async (flashcardId) => {
    const response = await api.get(`/users/me/flashcards/${flashcardId}/progress`);
    return response.data;
  },

  // Update progress
  updateProgress: async (flashcardId, progressData) => {
    const response = await api.put(`/users/me/flashcards/${flashcardId}/progress`, progressData);
    return response.data;
  },
};

export default progressService;
