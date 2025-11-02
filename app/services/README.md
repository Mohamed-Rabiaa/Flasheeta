# Service Layer Architecture

## Overview

The service layer provides a clean separation between business logic and route handlers (controllers). This architecture improves code organization, testability, and maintainability.

## Structure

```
app/services/
├── __init__.py
├── flashcard_service.py    # Flashcard business logic
├── deck_service.py          # Deck business logic
└── progress_service.py      # Progress tracking & SM2 algorithm
```

## Benefits

1. **Separation of Concerns**: Business logic is separated from HTTP handling
2. **Reusability**: Services can be used by both web routes and API endpoints
3. **Testability**: Services can be unit tested without HTTP context
4. **Consistency**: Centralized validation and error handling
5. **Maintainability**: Changes to business logic affect only one place

## Service Classes

### FlashcardService

Handles all flashcard-related operations:

- `create_flashcard(question, answer, deck_id)` - Creates flashcard with progress initialization
- `get_flashcard_by_id(flashcard_id)` - Retrieves single flashcard
- `get_flashcards_by_deck(deck_id)` - Gets all cards in a deck
- `update_flashcard(flashcard_id, question, answer, deck_id)` - Updates flashcard
- `delete_flashcard(flashcard_id)` - Deletes flashcard with cascade
- `get_due_flashcards(deck_id)` - Gets cards due for review
- `get_flashcard_with_progress(flashcard_id)` - Joins flashcard and progress
- `get_flashcards_by_user(user_id)` - Gets all user's flashcards
- `get_statistics(deck_id)` - Calculates deck statistics

**Example Usage:**

```python
from app.services.flashcard_service import FlashcardService

# Create a flashcard
try:
    flashcard = FlashcardService.create_flashcard(
        question="What is Python?",
        answer="A programming language",
        deck_id=deck.id
    )
except ValueError as e:
    flash(str(e))

# Get due flashcards
due_cards = FlashcardService.get_due_flashcards(deck.id)

# Get statistics
stats = FlashcardService.get_statistics(deck.id)
print(f"Total: {stats['total']}, Due: {stats['due']}")
```

### DeckService

Handles all deck-related operations:

- `create_deck(name, user_id, description)` - Creates deck with duplicate checking
- `get_deck_by_id(deck_id)` - Retrieves single deck
- `get_decks_by_user(user_id, order_by)` - Gets user's decks with ordering
- `update_deck(deck_id, name, description)` - Updates deck with validation
- `delete_deck(deck_id)` - Deletes deck with cascade
- `get_deck_with_statistics(deck_id)` - Enriches deck with statistics
- `verify_deck_ownership(deck_id, user_id)` - Authorization check
- `get_user_deck_count(user_id)` - Gets deck count

**Example Usage:**

```python
from app.services.deck_service import DeckService

# Create a deck
try:
    deck = DeckService.create_deck("Python Basics", current_user.id)
except ValueError as e:
    flash("Deck name already exists")

# Get decks with statistics
decks = DeckService.get_decks_by_user(current_user.id, order_by='name')
for deck in decks:
    enriched = DeckService.get_deck_with_statistics(deck.id)
    print(f"{enriched.name}: {enriched.total_cards} cards")

# Verify ownership before operations
if DeckService.verify_deck_ownership(deck_id, current_user.id):
    DeckService.delete_deck(deck_id)
```

### ProgressService

Handles progress tracking and spaced repetition:

- `get_progress(flashcard_id)` - Gets progress for a flashcard
- `update_progress(flashcard_id, progress_data)` - Updates progress fields
- `calculate_next_review(progress, rating)` - Hybrid SM2 algorithm calculation
- `get_user_statistics(user_id)` - Overall user statistics
- `reset_progress(flashcard_id)` - Resets card to initial state

**Example Usage:**

```python
from app.services.progress_service import ProgressService

# Get progress
progress = ProgressService.get_progress(flashcard_id)

# Calculate next review (hybrid SM2)
rating = 'good'  # 'again', 'hard', 'good', 'easy'
updates = ProgressService.calculate_next_review(progress, rating)

# Apply updates
updated_progress = ProgressService.update_progress(flashcard_id, updates)

# Get user statistics
stats = ProgressService.get_user_statistics(current_user.id)
print(f"Accuracy: {stats['accuracy']}%")
print(f"Due today: {stats['due_today']}")
print(f"Mastered: {stats['mastered']}")

# Reset progress
ProgressService.reset_progress(flashcard_id)
```

## Design Patterns

### Static Methods

Services use static methods since they don't maintain state:

```python
class FlashcardService:
    @staticmethod
    def create_flashcard(question: str, answer: str, deck_id: str) -> Flashcard:
        # Business logic here
        pass
```

### Type Hints

All service methods include type hints for better IDE support and documentation:

```python
@staticmethod
def get_flashcard_by_id(flashcard_id: str) -> Optional[Flashcard]:
    """
    Gets a flashcard by ID
    
    Args:
        flashcard_id: The flashcard ID
        
    Returns:
        Flashcard object or None if not found
    """
```

### Error Handling

Services raise `ValueError` for validation errors:

```python
if not question or not answer:
    raise ValueError("Question and answer cannot be empty")
```

Routes catch these and convert to appropriate HTTP responses:

```python
try:
    FlashcardService.create_flashcard(question, answer, deck_id)
    flash('Success!')
except ValueError as e:
    flash(str(e))
```

## Integration with Routes

### Before (Direct Model Access)

```python
@bp.route('/flashcards/new', methods=['POST'])
def new_flashcard():
    flashcard = Flashcard(
        question=form.front.data,
        answer=form.back.data,
        deck_id=deck_id
    )
    flashcard.save()
    
    progress = Progress(
        review_count=0,
        flashcard_id=flashcard.id
    )
    progress.save()
```

### After (Service Layer)

```python
@bp.route('/flashcards/new', methods=['POST'])
def new_flashcard():
    try:
        FlashcardService.create_flashcard(
            form.front.data,
            form.back.data,
            deck_id
        )
        flash('Success!')
    except ValueError as e:
        flash(str(e))
```

## Testing

Services are easy to unit test without HTTP context:

```python
def test_create_flashcard():
    # Setup
    deck = create_test_deck()
    
    # Test
    flashcard = FlashcardService.create_flashcard(
        "Test question",
        "Test answer",
        deck.id
    )
    
    # Assert
    assert flashcard.question == "Test question"
    assert flashcard.progress is not None
    assert flashcard.progress.review_count == 0

def test_create_flashcard_validation():
    deck = create_test_deck()
    
    with pytest.raises(ValueError, match="Question and answer cannot be empty"):
        FlashcardService.create_flashcard("", "", deck.id)
```

## Spaced Repetition Algorithm

The `ProgressService.calculate_next_review()` method implements a hybrid approach:

### Failed Cards (quality < 3)
- **Again (quality 0)**: 10 minutes
- **Hard (quality 2)**: 15 minutes
- Ease factor decreases by 0.2 (min 1.3)

### Successful Cards (quality >= 3)
- **Review 1**: 1 day
- **Review 2**: 6 days
- **Review 3+**: interval × ease_factor × multiplier
  - Good (quality 3): multiplier = 1.0
  - Easy (quality 5): multiplier = 1.3
- Ease factor adjusted based on quality

**Algorithm Implementation:**

```python
def calculate_next_review(progress: Progress, rating: str) -> Dict:
    quality = {'again': 0, 'hard': 2, 'good': 3, 'easy': 5}[rating]
    
    if quality < 3:
        # Fixed short intervals for failed cards
        interval = 10 if quality == 0 else 15  # minutes
        ease_factor = max(1.3, ease_factor - 0.2)
    else:
        # Adaptive SM2 for successful cards
        if review_count == 1:
            interval = 1  # day
        elif review_count == 2:
            interval = 6  # days
        else:
            multiplier = 1.3 if quality == 5 else 1.0
            interval = interval * ease_factor * multiplier
    
    return {
        'interval': interval,
        'ease_factor': ease_factor,
        'next_review_date': now + timedelta(days=interval),
        # ... other fields
    }
```

## Best Practices

1. **Keep services stateless** - Use static methods
2. **Single Responsibility** - Each service handles one domain entity
3. **Dependency Injection** - Services depend on models, not on each other
4. **Return domain objects** - Don't return HTTP responses
5. **Validate inputs** - Raise ValueError for invalid inputs
6. **Use type hints** - Improve IDE support and documentation
7. **Write docstrings** - Document parameters and return values
8. **Handle errors gracefully** - Return None or raise specific exceptions

## Future Enhancements

1. **Caching**: Add Redis caching for frequently accessed data
2. **Async operations**: Convert to async/await for better performance
3. **Event system**: Emit events for audit logging
4. **Dependency injection container**: Use Flask-Injector for DI
5. **Repository pattern**: Add data access layer between services and models
6. **Service composition**: Allow services to call other services
7. **Transactions**: Add transaction management for multi-step operations
8. **Logging**: Add structured logging for debugging
