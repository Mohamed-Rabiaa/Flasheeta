# Flasheeta - React Frontend Setup Guide

## ✅ Project Successfully Created!

Your React + Vite + React Router project is now set up with a complete folder structure.

## 📁 What's Been Created

### Core Files
- ✅ **Vite + React** project initialized
- ✅ **React Router v6** installed and configured
- ✅ **Axios** installed for API calls
- ✅ Complete folder structure created

### Services (API Layer)
- ✅ `services/api.js` - Axios configuration with interceptors
- ✅ `services/authService.js` - Login, register, logout
- ✅ `services/deckService.js` - Deck CRUD operations
- ✅ `services/flashcardService.js` - Flashcard CRUD
- ✅ `services/progressService.js` - Progress tracking

### State Management
- ✅ `context/AuthContext.jsx` - Authentication state
- ✅ `components/auth/ProtectedRoute.jsx` - Route protection

### Utilities
- ✅ `utils/constants.js` - App constants and configuration
- ✅ `utils/sm2Algorithm.js` - Spaced repetition algorithm (complete!)

### Routing
- ✅ `App.jsx` - Configured with all routes
- ✅ 8 placeholder page components created

## 🚀 Getting Started

### 1. Start Flask Backend
```bash
# Terminal 1 - Backend
cd i:\Work\Programming\Programming_Projects\Flasheeta
python run.py
```

### 2. Start React Dev Server
```bash
# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 3. Open in Browser
Navigate to: `http://localhost:5173`

## ⚙️ Backend Configuration Needed

Add CORS to your Flask app (`app/__init__.py`):

```python
from flask_cors import CORS

# After creating app
CORS(app, supports_credentials=True, origins=['http://localhost:5173'])
```

Install Flask-CORS if not already installed:
```bash
pip install flask-cors
```

## 📋 Next Steps - Development Phases

### Phase 1: Authentication (Week 1, Days 1-4)
**Files to implement:**
- `pages/LoginPage.jsx` - Login form
- `pages/RegisterPage.jsx` - Registration form

**What to add:**
- Form inputs and validation
- Connect to authService
- Handle errors and loading states
- Redirect after successful auth

### Phase 2: Deck Management (Week 1-2, Days 5-10)
**Files to implement:**
- `pages/DecksPage.jsx` - Main deck listing
- `components/deck/DeckCard.jsx` - Individual deck card
- `components/deck/DeckList.jsx` - Grid of decks
- `components/deck/DeckForm.jsx` - Create/edit modal
- `context/DeckContext.jsx` - Deck state management

**What to add:**
- Fetch and display decks
- Create new deck
- Edit deck
- Delete deck
- Show deck statistics

### Phase 3: Flashcard Management (Week 2, Days 11-17)
**Files to implement:**
- `pages/DeckDetailPage.jsx` - Deck with flashcards
- `pages/NewFlashcardPage.jsx` - Create flashcard
- `pages/EditFlashcardPage.jsx` - Edit flashcard
- `components/flashcard/FlashcardList.jsx`
- `components/flashcard/FlashcardItem.jsx`
- `components/flashcard/FlashcardForm.jsx`

**What to add:**
- Display flashcards in a deck
- Create new flashcard
- Edit flashcard
- Delete flashcard
- Navigate between deck and flashcards

### Phase 4: Review Session (Week 2-3, Days 18-24) ⚠️ MOST COMPLEX
**Files to implement:**
- `pages/ReviewPage.jsx` - Main review interface
- `components/review/ReviewSession.jsx` - Session logic
- `components/review/FlashcardViewer.jsx` - Card display with flip
- `components/review/RatingButtons.jsx` - Again/Hard/Good/Easy
- `components/review/ProgressBar.jsx` - Progress indicator
- `components/review/CompletionScreen.jsx` - End screen
- `context/ReviewContext.jsx` - Review state management

**What to add:**
- Card flipping animation
- Rating buttons with SM2 integration
- Card queue management
- Failed card re-queuing
- Progress tracking
- Session completion

### Phase 5: Profile & Polish (Week 3-4, Days 25-28)
**Files to implement:**
- `pages/ProfilePage.jsx` - User profile
- Common components (Button, Modal, Input, Card, Loader)
- Layout components (Header, Footer)

**What to add:**
- User statistics
- Profile settings
- Global header/navigation
- Consistent styling
- Error boundaries
- Loading states

## 🎨 Styling Options

Choose one:

### Option 1: Plain CSS (Simplest)
```bash
# No installation needed
# Use CSS modules: Component.module.css
```

### Option 2: Tailwind CSS (Recommended)
```bash
cd frontend
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Option 3: Material-UI (Component Library)
```bash
cd frontend
npm install @mui/material @emotion/react @emotion/styled
```

### Option 4: Ant Design (Component Library)
```bash
cd frontend
npm install antd
```

## 🗂️ Component Structure Example

```
DecksPage
├── Header (with nav and user menu)
└── Main Content
    ├── Page Title
    ├── Create Deck Button
    └── DeckList
        └── DeckCard[] (map over decks)
            ├── Deck name
            ├── Card count
            ├── Due cards
            └── Action buttons
```

## 📝 Code Example - Login Page

Here's what a completed LoginPage might look like:

```jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const result = await login(email, password);
    
    if (result.success) {
      navigate('/decks');
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: '400px', margin: '100px auto' }}>
      <h1>Login to Flasheeta</h1>
      <form onSubmit={handleSubmit}>
        {error && <div style={{color: 'red'}}>{error}</div>}
        
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      
      <p>
        Don't have an account? <a href="/register">Register</a>
      </p>
    </div>
  );
};

export default LoginPage;
```

## 🔍 Debugging Tips

### Check if backend is running:
```bash
curl http://localhost:5000/api/v1/users/me/decks
```

### Check CORS in browser console:
If you see CORS errors, make sure Flask-CORS is configured correctly.

### React DevTools:
Install React DevTools browser extension for easier debugging.

## 📚 Learning Resources

### React Router v6
- [Official Docs](https://reactrouter.com/)
- Tutorial: Routes, Links, Navigate, useParams, useNavigate

### React Context API
- [Official Docs](https://react.dev/reference/react/createContext)
- When to use Context vs props

### Axios
- [Official Docs](https://axios-http.com/)
- Interceptors, error handling

### React Hooks
- useState, useEffect, useContext, custom hooks
- [React Hooks Reference](https://react.dev/reference/react)

## 🆘 Common Issues

### Issue: "Module not found"
**Solution:** Make sure all imports use correct paths

### Issue: CORS errors
**Solution:** Add Flask-CORS configuration to backend

### Issue: 401 Unauthorized
**Solution:** Check that `withCredentials: true` is set in axios

### Issue: Routes not working
**Solution:** Make sure BrowserRouter wraps your app

## 📊 Project Timeline

| Week | Focus | Key Deliverables |
|------|-------|------------------|
| 1 | Auth + Decks | Login, Register, Deck list, Create deck |
| 2 | Flashcards | View, Create, Edit flashcards |
| 3 | Review | Review session with SM2 algorithm |
| 4 | Polish | Profile, styling, testing |

## ✨ You're All Set!

Your React frontend is ready for development. Start with Phase 1 (Authentication) and work your way through each phase systematically.

**Ready to start? Begin with implementing the LoginPage.jsx!**
