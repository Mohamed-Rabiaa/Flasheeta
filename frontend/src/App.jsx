import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/auth/ProtectedRoute';

// Pages (we'll create these next)
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DecksPage from './pages/DecksPage';
import DeckDetailPage from './pages/DeckDetailPage';
import ReviewPage from './pages/ReviewPage';
import ProfilePage from './pages/ProfilePage';
import NewFlashcardPage from './pages/NewFlashcardPage';
import EditFlashcardPage from './pages/EditFlashcardPage';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          
          {/* Protected Routes */}
          <Route path="/decks" element={
            <ProtectedRoute>
              <DecksPage />
            </ProtectedRoute>
          } />
          
          <Route path="/decks/:deckId" element={
            <ProtectedRoute>
              <DeckDetailPage />
            </ProtectedRoute>
          } />
          
          <Route path="/decks/:deckId/review" element={
            <ProtectedRoute>
              <ReviewPage />
            </ProtectedRoute>
          } />
          
          <Route path="/flashcards/new" element={
            <ProtectedRoute>
              <NewFlashcardPage />
            </ProtectedRoute>
          } />
          
          <Route path="/flashcards/:flashcardId/edit" element={
            <ProtectedRoute>
              <EditFlashcardPage />
            </ProtectedRoute>
          } />
          
          <Route path="/profile" element={
            <ProtectedRoute>
              <ProfilePage />
            </ProtectedRoute>
          } />
          
          {/* Default redirect */}
          <Route path="/" element={<Navigate to="/decks" replace />} />
          
          {/* 404 */}
          <Route path="*" element={<div>Page Not Found</div>} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
