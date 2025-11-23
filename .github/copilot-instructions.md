# Flasheeta Copilot Instructions

## Project Overview
Flasheeta is a Flask-based flashcard application with a service-layer architecture. It uses spaced repetition (SM2 algorithm) for optimal learning, featuring both web routes and a RESTful API.

## Architecture

### Service Layer Pattern (Critical)
**All business logic lives in services**, not routes. Routes handle HTTP concerns only.

- **Services**: `app/services/{flashcard,deck,progress}_service.py`
- **Web Routes**: `app/web_routes/` (render templates, handle forms)
- **API Routes**: `app/api/v1/views/` (JSON responses, CSRF exempt)

**Example pattern:**
```python
# ✅ Correct - Use service layer
from app.services.flashcard_service import FlashcardService
flashcard = FlashcardService.create_flashcard(question, answer, deck_id)

# ❌ Wrong - Don't manipulate models directly in routes
flashcard = Flashcard(question=question, answer=answer)
```

### Models & Storage
- **BaseModel**: All models inherit from `app/models/base_model.py` (UUID-based IDs, auto timestamps)
- **DBStorage**: Custom storage abstraction at `app/models/engine/db_storage.py`
- Access via `app.storage.get(Model, id)` or direct SQLAlchemy queries in services
- Models have `save()`, `delete()`, and `to_dict()` methods

### Error Handling (API Only)
Custom exceptions in `app/exceptions.py` automatically return JSON for `/api/*` routes:
- `ValidationError(400)` - Invalid input
- `NotFoundError(404)` - Missing resources
- `ConflictError(409)` - Duplicates
- `UnauthorizedError(401)`, `ForbiddenError(403)`, `ServerError(500)`

**Usage:** `raise NotFoundError("Flashcard not found")` (no try/catch needed in routes)

Web routes use Flask's `flash()` for user messages.

## Key Service Responsibilities

### FlashcardService
- `create_flashcard()` - Auto-creates Progress record with initial SM2 values
- `get_due_flashcards(deck_id)` - Filters by `next_review_date <= now()`
- `get_statistics(deck_id)` - Returns `{total, due, mastered, learning, new}` counts

### ProgressService
- `calculate_next_review(progress, rating)` - Hybrid SM2 algorithm implementation
- Ratings: `'again'(0)`, `'hard'(2)`, `'good'(3)`, `'easy'(5)`
- Updates `ease_factor`, `interval`, `next_review_date`

### DeckService
- `create_deck()` - Validates duplicate names per user
- `get_deck_with_statistics()` - Enriches deck with flashcard counts

## Frontend Architecture

### Modular JavaScript (app/static/scripts/)
- **config.js**: API endpoints, messages, constants
- **api-client.js**: All HTTP requests (CSRF token handling)
- **flashcard-manager.js**: Review state, queue logic
- **ui-manager.js**: DOM manipulation only
- **review-session.js**: Orchestrates manager + UI
- **sm2-algorithm.js**: Client-side spaced repetition

**Pattern:** Separation of concerns - API layer → Business logic → UI layer

## Development Workflows

### Environment Setup
```bash
pip install -r requirements.txt
# Set: SECRET_KEY (os.urandom(24).hex()), DATABASE_URL
flask db upgrade
```

### Running the App
```bash
python run.py  # Starts on localhost:5000
# Or with Docker: docker-compose up
```

### Database Migrations
```bash
flask db migrate -m "description"  # Generate migration
flask db upgrade                    # Apply migration
```

## Project-Specific Conventions

### Authentication & CSRF
- Web routes: Protected by `@login_required`, CSRF enabled
- API routes: Add `@csrf.exempt` decorator, still use `@login_required`
- Current user: `current_user.id` (Flask-Login)

### Date Handling
- Store UTC: `datetime.utcnow()`
- Progress dates: `last_review_date`, `next_review_date` (datetime objects)
- Parse ISO strings with `datetime.fromisoformat(date_str.replace('Z', '+00:00'))`

### Model Validation
- Services raise `ValidationError` for empty fields (question, answer, deck name)
- Deck names must be unique per user (`ConflictError` on duplicate)

### API Response Format
```python
# Success
return jsonify(flashcard.to_dict()), 201

# Error (handled automatically)
raise NotFoundError("Resource not found")  # Returns {"error": "...", "status_code": 404}
```

### Cascade Deletes
- Deleting a deck cascades to flashcards and progress (handled by services)
- Always use service methods: `DeckService.delete_deck(deck_id)`

## Critical Files to Reference

- **Service patterns**: `app/services/README.md` (comprehensive examples)
- **Error handling**: `ERROR_HANDLING_IMPLEMENTATION_SUMMARY.md`
- **Frontend arch**: `app/static/scripts/README.md`
- **SM2 algorithm**: `app/services/progress_service.py:calculate_next_review()`
- **App initialization**: `app/__init__.py` (blueprints, error handlers)

## Common Tasks

### Adding a New API Endpoint
1. Create method in appropriate service (`app/services/*.py`)
2. Add route in `app/api/v1/views/*.py`
3. Use `@csrf.exempt` and `@login_required`
4. Raise custom exceptions (not manual JSON errors)

### Adding a New Web Route
1. Create method in service if needed
2. Add route in `app/web_routes/*.py`
3. Use `flash()` for messages, `render_template()` for responses
4. Handle forms with `app/forms/*.py` (WTForms)

### Modifying the Review Algorithm
- Edit `ProgressService.calculate_next_review()` in `app/services/progress_service.py`
- Client-side preview: `app/static/scripts/sm2-algorithm.js`
- Rating scale is fixed: 0, 2, 3, 5 (don't change without updating both files)
