# API Error Handling Middleware

## Overview

The API Error Handling Middleware provides consistent, structured error responses across all API endpoints in the Flasheeta application. It centralizes error handling logic, making the codebase cleaner and API responses more predictable.

## Architecture

```
API Request
    ↓
Route Handler
    ↓
Service Layer (business logic)
    ↓
Exception Raised? → Yes → Error Handler Middleware → JSON Response
    ↓ No
Normal Response
```

## Components

### 1. Custom Exception Classes (`app/exceptions.py`)

Base exception and specific error types for different scenarios:

#### `APIException` (Base Class)
- Base class for all API exceptions
- Includes message, status_code, and optional payload
- Provides `to_dict()` method for JSON serialization

#### Specific Exception Classes

| Exception | HTTP Code | Use Case |
|-----------|-----------|----------|
| `ValidationError` | 400 | Invalid input data, validation failures |
| `NotFoundError` | 404 | Resource not found |
| `UnauthorizedError` | 401 | Authentication required |
| `ForbiddenError` | 403 | Insufficient permissions |
| `ConflictError` | 409 | Resource conflicts (duplicates) |
| `ServerError` | 500 | Internal server errors |

**Example Usage:**

```python
from app.exceptions import ValidationError, NotFoundError

# In service layer
if not question or not question.strip():
    raise ValidationError("Question cannot be empty")

if not flashcard:
    raise NotFoundError("Flashcard not found")
```

### 2. Error Handler Functions (`app/error_handlers.py`)

Registers error handlers with the Flask application:

#### Handler Functions

1. **`handle_api_exception(error)`**
   - Handles all custom `APIException` subclasses
   - Returns JSON with error details
   - Logs warnings for debugging

2. **`handle_value_error(error)`**
   - Catches `ValueError` from legacy code
   - Converts to 400 Bad Request
   - Gradually being replaced by `ValidationError`

3. **HTTP Status Code Handlers**
   - `handle_not_found(404)` - Resource not found
   - `handle_unauthorized(401)` - Authentication required
   - `handle_forbidden(403)` - Permission denied
   - `handle_method_not_allowed(405)` - Invalid HTTP method
   - `handle_unprocessable_entity(422)` - Invalid data format
   - `handle_internal_error(500)` - Server errors

4. **`handle_unexpected_error(error)`**
   - Catches any unexpected exceptions
   - Prevents application crashes
   - Returns generic error in production (detailed in debug mode)

**Important:** All handlers check if the request path starts with `/api/` before returning JSON. This allows web routes to handle errors normally with HTML pages.

### 3. Integration with Flask App

The error handlers are registered in `app/__init__.py`:

```python
# Register error handlers
from app.error_handlers import register_error_handlers
register_error_handlers(app)
```

This is called during application initialization, after blueprints are registered.

## Error Response Format

### Standard Error Response

```json
{
  "error": "Error message",
  "status_code": 400
}
```

### Error Response with Details

```json
{
  "error": "Validation failed",
  "status_code": 400,
  "details": {
    "field": "question",
    "reason": "Field cannot be empty"
  }
}
```

### HTTP-Specific Errors

```json
{
  "error": "Resource not found",
  "status_code": 404,
  "path": "/api/v1/users/me/flashcards/invalid-id"
}
```

## Usage in Services

### Before (Manual Error Handling)

```python
@staticmethod
def create_flashcard(question, answer, deck_id):
    if not question:
        raise ValueError("Question cannot be empty")
    # ... rest of logic
```

Route handler had to catch and convert:

```python
try:
    flashcard = FlashcardService.create_flashcard(...)
except ValueError as e:
    return jsonify({'error': str(e)}), 400
```

### After (With Middleware)

Service:
```python
from app.exceptions import ValidationError

@staticmethod
def create_flashcard(question, answer, deck_id):
    if not question:
        raise ValidationError("Question cannot be empty")
    # ... rest of logic
```

Route handler (simplified):
```python
# Exception is automatically caught and converted to JSON
flashcard = FlashcardService.create_flashcard(...)
return jsonify(flashcard.to_dict()), 201
```

## Common Patterns

### 1. Input Validation

```python
from app.exceptions import ValidationError

if not name or not name.strip():
    raise ValidationError("Name cannot be empty")

if len(name) > 100:
    raise ValidationError("Name too long (max 100 characters)")
```

### 2. Resource Not Found

```python
from app.exceptions import NotFoundError

flashcard = FlashcardService.get_flashcard_by_id(flashcard_id)
if not flashcard:
    raise NotFoundError("Flashcard not found")
```

### 3. Duplicate/Conflict Detection

```python
from app.exceptions import ConflictError

existing_deck = Deck.query.filter_by(name=name, user_id=user_id).first()
if existing_deck:
    raise ConflictError(f"Deck with name '{name}' already exists")
```

### 4. Authorization Checks

```python
from app.exceptions import ForbiddenError

if deck.user_id != current_user.id:
    raise ForbiddenError("You don't have permission to access this deck")
```

### 5. Error with Additional Context

```python
from app.exceptions import ValidationError

raise ValidationError(
    "Invalid flashcard data",
    payload={
        "errors": {
            "question": "Must be at least 5 characters",
            "answer": "Cannot be empty"
        }
    }
)
```

## Benefits

### 1. **Consistency**
- All API errors follow the same format
- Predictable client-side error handling
- Uniform status codes across endpoints

### 2. **Cleaner Code**
- No repetitive try/catch blocks in routes
- Service layer focuses on business logic
- Reduced boilerplate code

### 3. **Better Debugging**
- Centralized logging of all errors
- Stack traces captured in logs
- Easier to track error patterns

### 4. **Type Safety**
- Clear exception types indicate error categories
- IDE autocomplete for exception classes
- Self-documenting error handling

### 5. **Maintainability**
- Single place to modify error response format
- Easy to add new error types
- Consistent behavior across application

## Logging

All errors are logged with appropriate levels:

- **WARNING**: Client errors (4xx) - ValidationError, NotFoundError
- **ERROR**: Server errors (5xx) - ServerError, unexpected exceptions
- **INFO**: Informational (404 on API routes)

Example log output:
```
WARNING: API Exception: Question cannot be empty (status_code=400)
ERROR: Unexpected error: division by zero
INFO: 404 Not Found: /api/v1/users/me/flashcards/invalid-id
```

## Testing

### Unit Testing Error Handlers

```python
def test_validation_error_handler(client):
    # Trigger validation error
    response = client.post('/api/v1/flashcards', json={})
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['status_code'] == 400
```

### Testing Service Exceptions

```python
def test_create_flashcard_validation():
    with pytest.raises(ValidationError) as exc_info:
        FlashcardService.create_flashcard("", "", deck_id)
    
    assert "cannot be empty" in str(exc_info.value.message)
    assert exc_info.value.status_code == 400
```

## Migration Guide

### Updating Existing Services

1. **Add import:**
   ```python
   from app.exceptions import ValidationError, NotFoundError, ConflictError
   ```

2. **Replace ValueError with specific exceptions:**
   ```python
   # Before
   raise ValueError("Invalid input")
   
   # After
   raise ValidationError("Invalid input")
   ```

3. **Replace None checks with NotFoundError:**
   ```python
   # Before
   if not resource:
       return None
   
   # After
   if not resource:
       raise NotFoundError("Resource not found")
   ```

### Updating Existing Routes

1. **Remove try/catch blocks:**
   ```python
   # Before
   try:
       result = SomeService.do_something()
       return jsonify(result), 200
   except ValueError as e:
       return jsonify({'error': str(e)}), 400
   
   # After
   result = SomeService.do_something()
   return jsonify(result), 200
   ```

2. **Remove manual error responses:**
   ```python
   # Before
   if not flashcard:
       return jsonify({'error': 'Not Found'}), 404
   
   # After
   if not flashcard:
       raise NotFoundError('Flashcard not found')
   ```

## Files Modified

### New Files Created
1. `app/exceptions.py` - Custom exception classes
2. `app/error_handlers.py` - Error handler registration
3. `app/services/ERROR_HANDLING.md` - This documentation

### Modified Files
1. `app/__init__.py` - Register error handlers
2. `app/services/flashcard_service.py` - Use ValidationError
3. `app/services/deck_service.py` - Use ValidationError, ConflictError
4. `app/api/v1/views/flashcards.py` - Raise NotFoundError
5. `app/api/v1/views/progress.py` - Raise NotFoundError, ValidationError

## HTTP Status Code Reference

| Code | Meaning | When to Use |
|------|---------|-------------|
| 400 | Bad Request | Invalid input, validation failures |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | User lacks permissions |
| 404 | Not Found | Resource doesn't exist |
| 405 | Method Not Allowed | Wrong HTTP method (GET vs POST) |
| 409 | Conflict | Duplicate resource, state conflict |
| 422 | Unprocessable Entity | Valid format but invalid data |
| 500 | Internal Server Error | Server-side bug, unexpected error |

## Best Practices

1. **Use Specific Exceptions**: Choose the most appropriate exception type
2. **Provide Context**: Include helpful error messages
3. **Don't Leak Sensitive Info**: Avoid exposing internal details in production
4. **Log Appropriately**: Use correct log levels
5. **Test Error Paths**: Write tests for error scenarios
6. **Document Errors**: Include possible errors in API documentation
7. **Be Consistent**: Follow established patterns

## Future Enhancements

1. **Rate Limiting**: Add 429 Too Many Requests handler
2. **Request Validation**: Add JSON schema validation middleware
3. **Error Codes**: Add machine-readable error codes
4. **Internationalization**: Support multiple languages for error messages
5. **Metrics**: Track error rates by type and endpoint
6. **Retryable Errors**: Flag errors that clients can retry

## Date
November 3, 2025
