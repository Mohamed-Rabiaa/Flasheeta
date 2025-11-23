import api from './api';

const deckService = {
  // Get all decks for current user
  getDecks: async () => {
    const response = await api.get('/users/me/decks');
    return response.data;
  },

  // Get single deck by ID
  getDeck: async (deckId) => {
    const response = await api.get(`/users/me/decks/${deckId}`);
    return response.data;
  },

  // Create new deck
  createDeck: async (deckData) => {
    const response = await api.post('/users/me/decks', deckData);
    return response.data;
  },

  // Update deck
  updateDeck: async (deckId, deckData) => {
    const response = await api.put(`/users/me/decks/${deckId}`, deckData);
    return response.data;
  },

  // Delete deck
  deleteDeck: async (deckId) => {
    const response = await api.delete(`/users/me/decks/${deckId}`);
    return response.data;
  },
};

export default deckService;
