// App-wide constants
export const CONFIG = {
  API_BASE_URL: 'http://localhost:5000/api/v1',
  
  // Review intervals (in minutes for failed cards)
  INTERVALS: {
    AGAIN: 10,  // 10 minutes
    HARD: 15,   // 15 minutes
  },
  
  // SM2 Algorithm defaults
  SM2: {
    INITIAL_EASE_FACTOR: 2.5,
    MIN_EASE_FACTOR: 1.3,
    MAX_EASE_FACTOR: 2.5,
  },
  
  // Messages
  MESSAGES: {
    DECK_COMPLETE: 'Congratulations! You have completed reviewing all cards in this deck.',
    LOGIN_REQUIRED: 'Please log in to continue',
    ERROR_GENERIC: 'An error occurred. Please try again.',
  },
  
  // Debug mode (set to false in production)
  DEBUG: true,
};

// Rating values mapping
export const RATINGS = {
  AGAIN: 0,
  HARD: 2,
  GOOD: 3,
  EASY: 5,
};

// Card status
export const CARD_STATUS = {
  NEW: 'new',
  LEARNING: 'learning',
  MASTERED: 'mastered',
};
