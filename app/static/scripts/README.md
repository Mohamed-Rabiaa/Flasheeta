# Frontend JavaScript Architecture

## Overview
The frontend has been refactored into a modular architecture for better maintainability, testability, and code organization.

## File Structure

```
app/static/scripts/
├── config.js              # Configuration constants
├── api-client.js          # API communication layer
├── flashcard-manager.js   # Business logic for flashcard state
├── ui-manager.js          # DOM manipulation and UI rendering
├── review-session.js      # Review session orchestration
├── app.js                 # Main application entry point
├── sm2-algorithm.js       # Spaced repetition algorithm (unchanged)
└── navbar_link_color.js   # Navbar utilities (unchanged)
```

## Module Responsibilities

### 1. **config.js**
- Application configuration constants
- API endpoints
- UI messages
- Interval settings
- Debug flags

**Usage:**
```javascript
CONFIG.API.BASE_URL        // API base URL
CONFIG.MESSAGES.NO_DECKS   // UI messages
CONFIG.DEBUG               // Debug mode flag
```

### 2. **api-client.js**
- All HTTP requests to backend API
- Error handling for network requests
- CSRF token management

**API:**
```javascript
await FlashcardAPI.getDecks()
await FlashcardAPI.getFlashcards(deckId)
await FlashcardAPI.getProgress(flashcardId)
await FlashcardAPI.updateProgress(flashcardId, progressData)
await FlashcardAPI.deleteFlashcard(flashcardId)
```

### 3. **flashcard-manager.js**
- Manages flashcard review state
- Handles review queue logic
- Tracks immediate review cards
- Manages session progression

**API:**
```javascript
const manager = new FlashcardManager(deckId, flashcards)
manager.getCurrentFlashcard()
manager.isSessionComplete()
manager.isCardDue(progress)
manager.markForImmediateReview()
manager.moveToNext()
manager.handleEndOfDeck()
manager.getStats()
```

### 4. **ui-manager.js**
- All DOM manipulation
- UI component rendering
- Flashcard display logic
- Empty states and messages

**API:**
```javascript
UIManager.showEmptyState(message)
UIManager.renderDeck(deck, onClick)
UIManager.initFlashcardView()
UIManager.showFlashcard(flashcard)
UIManager.showAnswer(answer)
UIManager.resetFlashcardView()
UIManager.showCompletionMessage()
```

### 5. **review-session.js**
- Orchestrates the review session
- Coordinates between manager and UI
- Handles user interactions (ratings, delete, edit)
- Progress updates

**API:**
```javascript
const session = new ReviewSession(deckId, flashcards)
await session.start()
```

### 6. **app.js**
- Application entry point
- Initializes jQuery
- Loads decks
- Starts review sessions

## Benefits of Modular Architecture

### ✅ **Separation of Concerns**
Each module has a single, well-defined responsibility:
- API Client → Network requests
- Manager → Business logic
- UI Manager → Presentation
- Session → Orchestration

### ✅ **Testability**
Modules can be tested independently:
```javascript
// Example unit test
describe('FlashcardManager', () => {
  test('marks card for immediate review', () => {
    const manager = new FlashcardManager('deck-1', mockFlashcards);
    manager.markForImmediateReview();
    expect(manager.immediateReviewCards.size).toBe(1);
  });
});
```

### ✅ **Reusability**
Modules can be reused across different pages:
```javascript
// Use API client from any page
await FlashcardAPI.getDecks()
```

### ✅ **Maintainability**
- Clear file structure
- Easy to locate specific functionality
- Reduced complexity per file
- Better code organization

### ✅ **Debugging**
- Isolated modules make bugs easier to find
- Debug mode for detailed logging
- Clear error boundaries

## Migration from Old Code

### Old Structure (all_decks.js - 277 lines)
- Everything in one large file
- Deeply nested functions
- Mixed concerns
- Hard to test
- Difficult to maintain

### New Structure (6 focused modules)
- Clear separation of concerns
- Flat, manageable files
- Easy to test
- Easy to extend
- Self-documenting

## Adding New Features

### Example: Adding a "Skip" button

1. **UI Manager** - Add the button HTML:
```javascript
static getFlashcardHtml() {
    // Add skip button to template
}
```

2. **Review Session** - Add event handler:
```javascript
setupEventHandlers() {
    $(document).on('click', 'button.skip', () => {
        this.handleSkip();
    });
}

handleSkip() {
    this.manager.moveToNext();
    await this.showNextFlashcard();
}
```

That's it! The modular architecture makes additions clean and simple.

## Debug Mode

Set `CONFIG.DEBUG = true` for detailed logging:
- API requests and responses
- State transitions
- Progress updates
- Session statistics

## Best Practices

1. **Keep modules focused** - Each file should have one clear responsibility
2. **Use classes** - Organize related functionality into classes
3. **Document public APIs** - Add JSDoc comments for all public methods
4. **Handle errors** - Always wrap async operations in try-catch
5. **Log appropriately** - Use debug mode for development logging

## Future Improvements

- [ ] Add TypeScript for type safety
- [ ] Add unit tests for each module
- [ ] Bundle modules with webpack/rollup
- [ ] Add loading states and animations
- [ ] Implement offline support
- [ ] Add keyboard shortcuts

## Backwards Compatibility

The old `all_decks.js` has been backed up as `all_decks.js.backup`. 
The new modular code provides the same functionality with improved architecture.
