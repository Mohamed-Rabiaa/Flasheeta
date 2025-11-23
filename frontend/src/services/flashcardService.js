import api from './api';

const flashcardService = {
  // Get all flashcards for a deck
  getFlashcards: async (deckId) => {
    const response = await api.get(`/users/me/decks/${deckId}/flashcards`);
    return response.data;
  },

  // Get single flashcard
  getFlashcard: async (flashcardId) => {
    const response = await api.get(`/users/me/flashcards/${flashcardId}`);
    return response.data;
  },

  // Create flashcard
  createFlashcard: async (flashcardData) => {
    const response = await api.post('/users/me/flashcards', flashcardData);
    return response.data;
  },

  // Update flashcard
  updateFlashcard: async (flashcardId, flashcardData) => {
    const response = await api.put(`/users/me/flashcards/${flashcardId}`, flashcardData);
    return response.data;
  },

  // Delete flashcard
  deleteFlashcard: async (flashcardId) => {
    const response = await api.delete(`/users/me/flashcards/${flashcardId}`);
    return response.data;
  },
};

export default flashcardService;
