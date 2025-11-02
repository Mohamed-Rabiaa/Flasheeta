/**
 * FLASHEETA FRONTEND ARCHITECTURE
 * ================================
 * 
 * Modular JavaScript architecture with clear separation of concerns
 * 
 * 
 * ┌─────────────────────────────────────────────────────────────┐
 * │                         app.js                              │
 * │                  (Application Entry Point)                   │
 * │  • Initializes jQuery                                        │
 * │  • Loads decks on page load                                  │
 * │  • Starts review sessions                                    │
 * └────────────────────┬────────────────────────────────────────┘
 *                      │
 *                      ├── Uses ──────────────────────┐
 *                      │                               │
 *                      ▼                               ▼
 * ┌──────────────────────────────┐    ┌──────────────────────────────┐
 * │    FlashcardAPI              │    │      UIManager               │
 * │    (api-client.js)           │    │      (ui-manager.js)         │
 * │                              │    │                              │
 * │  • getDecks()                │    │  • renderDeck()              │
 * │  • getFlashcards()           │    │  • showEmptyState()          │
 * │  • getProgress()             │    │  • initFlashcardView()       │
 * │  • updateProgress()          │    │  • showFlashcard()           │
 * │  • deleteFlashcard()         │    │  • showAnswer()              │
 * │                              │    │  • resetFlashcardView()      │
 * └──────────────────────────────┘    └──────────────────────────────┘
 *                ▲                                   ▲
 *                │                                   │
 *                │    Used by                        │    Used by
 *                │                                   │
 * ┌──────────────┴───────────────────────────────────┴────────────┐
 * │                    ReviewSession                              │
 * │                  (review-session.js)                          │
 * │                                                               │
 * │  • Orchestrates flashcard review                             │
 * │  • Handles user interactions (ratings, delete, edit)         │
 * │  • Coordinates between FlashcardManager and UI               │
 * │                                                               │
 * │  Methods:                                                     │
 * │    - start()                                                  │
 * │    - showNextFlashcard()                                      │
 * │    - handleRating(rating)                                     │
 * │    - handleDelete()                                           │
 * │    - handleEdit()                                             │
 * └────────────────────────┬──────────────────────────────────────┘
 *                          │
 *                          │ Uses
 *                          │
 *                          ▼
 * ┌─────────────────────────────────────────────────────────────┐
 * │                  FlashcardManager                           │
 * │                (flashcard-manager.js)                        │
 * │                                                              │
 * │  • Manages review session state                             │
 * │  • Tracks current flashcard index                           │
 * │  • Manages review queue                                     │
 * │  • Handles immediate review cards                           │
 * │                                                              │
 * │  Methods:                                                    │
 * │    - getCurrentFlashcard()                                   │
 * │    - isSessionComplete()                                     │
 * │    - isCardDue(progress)                                     │
 * │    - markForImmediateReview()                               │
 * │    - moveToNext()                                            │
 * │    - handleEndOfDeck()                                       │
 * │    - shouldBypassDateCheck()                                │
 * │    - getStats()                                              │
 * └─────────────────────────────────────────────────────────────┘
 * 
 * 
 * ┌─────────────────────────────────────────────────────────────┐
 * │                         config.js                            │
 * │                  (Configuration Constants)                    │
 * │                                                              │
 * │  • API_BASE_URL                                              │
 * │  • INTERVALS (again, hard)                                   │
 * │  • MESSAGES (UI strings)                                     │
 * │  • DEBUG flag                                                │
 * └─────────────────────────────────────────────────────────────┘
 *          ▲
 *          │ Used by all modules
 *          │
 * 
 * ┌─────────────────────────────────────────────────────────────┐
 * │                    sm2-algorithm.js                          │
 * │              (Spaced Repetition Algorithm)                   │
 * │                                                              │
 * │  • sm2Algorithm()                                            │
 * │  • validateProgress()                                        │
 * │  • getNextReviewDescription()                               │
 * │  • calculateLearningStats()                                 │
 * └─────────────────────────────────────────────────────────────┘
 *          ▲
 *          │ Used by ReviewSession
 *          │
 * 
 * 
 * DATA FLOW:
 * ==========
 * 
 * 1. User clicks on a deck
 *    app.js → FlashcardAPI.getFlashcards()
 * 
 * 2. Create review session
 *    app.js → new ReviewSession(deckId, flashcards)
 * 
 * 3. Show first flashcard
 *    ReviewSession.start() → FlashcardManager.getCurrentFlashcard()
 *                         → FlashcardAPI.getProgress()
 *                         → UIManager.showFlashcard()
 * 
 * 4. User rates flashcard
 *    UI Button Click → ReviewSession.handleRating()
 *                   → sm2Algorithm()
 *                   → FlashcardAPI.updateProgress()
 *                   → FlashcardManager.moveToNext()
 *                   → ReviewSession.showNextFlashcard()
 * 
 * 5. Session complete
 *    FlashcardManager.isSessionComplete()
 *    → UIManager.showCompletionMessage()
 * 
 * 
 * BENEFITS:
 * =========
 * 
 * ✅ Separation of Concerns
 *    - Each module has a single responsibility
 *    - Clear boundaries between components
 * 
 * ✅ Testability
 *    - Modules can be tested independently
 *    - Easy to mock dependencies
 * 
 * ✅ Maintainability
 *    - Easy to locate and fix bugs
 *    - Clear code organization
 * 
 * ✅ Reusability
 *    - Modules can be used across different pages
 *    - API client can be shared
 * 
 * ✅ Scalability
 *    - Easy to add new features
 *    - Simple to extend functionality
 */
