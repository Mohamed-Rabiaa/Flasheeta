#!/usr/bin/python3
"""
Flashcard Service Layer
Handles business logic for flashcard operations
"""

from datetime import datetime
from typing import List, Optional, Dict
from app.models.flashcard import Flashcard
from app.models.progress import Progress
from app.models.deck import Deck
from app.exceptions import ValidationError, NotFoundError
from flask import current_app as app


class FlashcardService:
    """Service class for flashcard-related operations"""

    @staticmethod
    def create_flashcard(question: str, answer: str, deck_id: str) -> Flashcard:
        """
        Creates a new flashcard with initial progress tracking
        
        Args:
            question: The flashcard question text
            answer: The flashcard answer text
            deck_id: The ID of the deck to add the flashcard to
            
        Returns:
            The created Flashcard object
            
        Raises:
            ValueError: If question or answer is empty
        """
        # Validate inputs
        if not question or not question.strip():
            raise ValidationError("Question cannot be empty")
        if not answer or not answer.strip():
            raise ValidationError("Answer cannot be empty")
        
        # Create flashcard
        flashcard = Flashcard(
            question=question.strip(),
            answer=answer.strip(),
            deck_id=deck_id
        )
        flashcard.save()
        
        # Initialize progress tracking
        progress = Progress(
            review_count=0,
            correct_count=0,
            flashcard_id=flashcard.id,
            last_review_date=datetime.utcnow(),
            next_review_date=datetime.utcnow()  # Due immediately
        )
        progress.save()
        
        return flashcard

    @staticmethod
    def get_flashcard_by_id(flashcard_id: str) -> Optional[Flashcard]:
        """
        Retrieves a flashcard by its ID
        
        Args:
            flashcard_id: The flashcard ID
            
        Returns:
            Flashcard object or None if not found
        """
        return app.storage.get(Flashcard, flashcard_id)

    @staticmethod
    def get_flashcards_by_deck(deck_id: str) -> List[Flashcard]:
        """
        Retrieves all flashcards for a specific deck
        
        Args:
            deck_id: The deck ID
            
        Returns:
            List of Flashcard objects
        """
        from app import db
        return db.session.query(Flashcard).filter_by(deck_id=deck_id).all()

    @staticmethod
    def update_flashcard(flashcard_id: str, question: Optional[str] = None, 
                        answer: Optional[str] = None, deck_id: Optional[str] = None) -> Optional[Flashcard]:
        """
        Updates a flashcard's content
        
        Args:
            flashcard_id: The flashcard ID
            question: New question text (optional)
            answer: New answer text (optional)
            deck_id: New deck ID (optional)
            
        Returns:
            Updated Flashcard object or None if not found
            
        Raises:
            ValueError: If trying to set empty question or answer
        """
        flashcard = app.storage.get(Flashcard, flashcard_id)
        if not flashcard:
            return None
        
        if question is not None:
            if not question.strip():
                raise ValueError("Question cannot be empty")
            flashcard.question = question.strip()
        
        if answer is not None:
            if not answer.strip():
                raise ValueError("Answer cannot be empty")
            flashcard.answer = answer.strip()
        
        if deck_id is not None:
            flashcard.deck_id = deck_id
        
        flashcard.save()
        return flashcard

    @staticmethod
    def delete_flashcard(flashcard_id: str) -> bool:
        """
        Deletes a flashcard and its associated progress
        
        Args:
            flashcard_id: The flashcard ID
            
        Returns:
            True if deleted, False if not found
        """
        flashcard = app.storage.get(Flashcard, flashcard_id)
        if not flashcard:
            return False
        
        # Delete flashcard (cascade will automatically delete associated progress)
        app.storage.delete(flashcard)
        app.storage.save()
        return True

    @staticmethod
    def get_due_flashcards(deck_id: str) -> List[Flashcard]:
        """
        Gets flashcards that are due for review in a deck
        
        Args:
            deck_id: The deck ID
            
        Returns:
            List of Flashcard objects that are due for review
        """
        from app import db
        now = datetime.utcnow()
        
        flashcards = db.session.query(Flashcard)\
            .join(Progress)\
            .filter(Flashcard.deck_id == deck_id)\
            .filter(Progress.next_review_date <= now)\
            .all()
        
        return flashcards

    @staticmethod
    def get_flashcard_with_progress(flashcard_id: str) -> Optional[Dict]:
        """
        Gets a flashcard with its progress data
        
        Args:
            flashcard_id: The flashcard ID
            
        Returns:
            Dictionary with flashcard and progress data, or None if not found
        """
        flashcard = app.storage.get(Flashcard, flashcard_id)
        if not flashcard:
            return None
        
        result = flashcard.to_dict()
        if flashcard.progress:
            result['progress'] = flashcard.progress.to_dict()
        
        return result

    @staticmethod
    def get_flashcards_by_user(user_id: str, limit: Optional[int] = None) -> List[Flashcard]:
        """
        Gets all flashcards for a user across all their decks
        
        Args:
            user_id: The user ID
            limit: Optional limit on number of flashcards
            
        Returns:
            List of Flashcard objects
        """
        from app import db
        
        query = db.session.query(Flashcard)\
            .join(Deck)\
            .filter(Deck.user_id == user_id)
        
        if limit:
            query = query.limit(limit)
        
        return query.all()

    @staticmethod
    def get_statistics(deck_id: str) -> Dict:
        """
        Gets statistics for a deck
        
        Args:
            deck_id: The deck ID
            
        Returns:
            Dictionary with statistics (total, due, mastered, etc.)
        """
        from app import db
        now = datetime.utcnow()
        
        flashcards = FlashcardService.get_flashcards_by_deck(deck_id)
        total = len(flashcards)
        
        if total == 0:
            return {
                'total': 0,
                'due': 0,
                'mastered': 0,
                'learning': 0,
                'new': 0
            }
        
        due = 0
        mastered = 0  # Reviewed 5+ times with high ease factor
        learning = 0  # Currently being learned
        new = 0       # Never reviewed
        
        for flashcard in flashcards:
            if flashcard.progress:
                progress = flashcard.progress
                
                # Check if due
                if progress.next_review_date <= now:
                    due += 1
                
                # Categorize
                if progress.review_count == 0:
                    new += 1
                elif progress.review_count >= 5 and progress.ease_factor >= 2.5:
                    mastered += 1
                else:
                    learning += 1
        
        return {
            'total': total,
            'due': due,
            'mastered': mastered,
            'learning': learning,
            'new': new
        }
