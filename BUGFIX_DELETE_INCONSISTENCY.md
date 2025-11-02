# Bug Fix: Flashcard Deletion UI Inconsistency

## Issue Description

When deleting a flashcard during a review session:
- The next card would briefly show the deleted card's answer
- Then show the correct card's answer twice instead of once
- This created a confusing user experience

## Root Cause Analysis

The problem had multiple contributing factors:

1. **Array Management**: When a card was deleted, it remained in the `flashcards` array but `currentIndex` was incremented, causing index misalignment
2. **UI State**: The `resetFlashcardView()` method wasn't clearing the question text, leaving stale data in the DOM
3. **Event Handlers**: The show-answer button handlers weren't being properly cleaned up between cards

## Solution

### 1. Added `removeCurrentFlashcard()` Method to FlashcardManager

```javascript
removeCurrentFlashcard() {
    const currentCard = this.getCurrentFlashcard();
    if (!currentCard) return;

    // Remove from main flashcards array
    this.flashcards.splice(this.currentIndex, 1);
    
    // Remove from review queues if present
    this.reviewAgainFlashcards = this.reviewAgainFlashcards.filter(
        card => card.id !== currentCard.id
    );
    this.immediateReviewCards.delete(currentCard.id);
    
    // Don't increment index - next card is now at current position
}
```

**Key Insight**: After `splice()`, the next card automatically moves to the current index position, so we don't need to increment.

### 2. Updated `handleDelete()` in ReviewSession

```javascript
async handleDelete() {
    // ... confirmation logic ...
    
    await FlashcardAPI.deleteFlashcard(flashcard.id);
    
    // Remove card from manager (doesn't increment index) ← NEW
    this.manager.removeCurrentFlashcard();
    
    // Reset UI to clear any stale data ← NEW
    UIManager.resetFlashcardView();
    
    // Show next card
    await this.showNextFlashcard();
}
```

**Changes**:
- Replaced `moveToNext()` with `removeCurrentFlashcard()`
- Added explicit `resetFlashcardView()` call before showing next card

### 3. Improved `resetFlashcardView()` in UIManager

```javascript
static resetFlashcardView() {
    $('p.flashcard-question').css('border-bottom', '').text(''); ← Added .text('')
    $('p.flashcard-answer').remove();
    $('div.rating-container').remove();
    
    // Re-enable the show-answer button ← NEW
    $('button.show-answer').off('click');
}
```

**Changes**:
- Now clears the question text completely
- Removes all event handlers from show-answer button

## Files Modified

1. `app/static/scripts/flashcard-manager.js`
   - Added `removeCurrentFlashcard()` method

2. `app/static/scripts/review-session.js`
   - Updated `handleDelete()` to use new removal method
   - Added explicit UI reset call

3. `app/static/scripts/ui-manager.js`
   - Improved `resetFlashcardView()` to clear question text and handlers

## Testing Checklist

- [x] Delete a card and verify next card shows correct question
- [x] Delete a card and verify answer appears only once when clicking "Show Answer"
- [x] Delete multiple cards in sequence
- [x] Delete a card that was marked for immediate review
- [x] Delete a card at the end of the deck
- [x] Verify deleted cards don't reappear in review queue

## Impact

✅ **Fixed**: UI now correctly displays the next card after deletion
✅ **Fixed**: No more duplicate answers showing
✅ **Fixed**: Clean state management when removing cards
✅ **Improved**: Better separation of concerns (deletion logic in manager, UI logic in UIManager)

## Date
November 2, 2025
