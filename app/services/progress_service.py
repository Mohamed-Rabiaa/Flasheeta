#!/usr/bin/python3
"""
Progress Service Layer
Handles business logic for progress tracking and spaced repetition
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, List
from app.models.progress import Progress
from app.models.flashcard import Flashcard
from flask import current_app as app


class ProgressService:
    """Service class for progress and spaced repetition operations"""

    @staticmethod
    def get_progress(flashcard_id: str) -> Optional[Progress]:
        """
        Gets the progress for a flashcard
        
        Args:
            flashcard_id: The flashcard ID
            
        Returns:
            Progress object or None if not found
        """
        from app import db
        return db.session.query(Progress).filter_by(flashcard_id=flashcard_id).first()

    @staticmethod
    def update_progress(flashcard_id: str, progress_data: Dict) -> Optional[Progress]:
        """
        Updates progress for a flashcard
        
        Args:
            flashcard_id: The flashcard ID
            progress_data: Dictionary with progress fields to update
            
        Returns:
            Updated Progress object or None if not found
        """
        progress = ProgressService.get_progress(flashcard_id)
        if not progress:
            return None
        
        # Update fields
        if 'review_count' in progress_data:
            progress.review_count = progress_data['review_count']
        
        if 'correct_count' in progress_data:
            progress.correct_count = progress_data['correct_count']
        
        if 'ease_factor' in progress_data:
            progress.ease_factor = progress_data['ease_factor']
        
        if 'interval' in progress_data:
            progress.interval = progress_data['interval']
        
        if 'last_review_date' in progress_data:
            if isinstance(progress_data['last_review_date'], str):
                progress.last_review_date = datetime.fromisoformat(
                    progress_data['last_review_date'].replace('Z', '+00:00')
                )
            else:
                progress.last_review_date = progress_data['last_review_date']
        
        if 'next_review_date' in progress_data:
            if isinstance(progress_data['next_review_date'], str):
                progress.next_review_date = datetime.fromisoformat(
                    progress_data['next_review_date'].replace('Z', '+00:00')
                )
            else:
                progress.next_review_date = progress_data['next_review_date']
        
        if 'difficulty_rating' in progress_data:
            progress.difficulty_rating = progress_data['difficulty_rating']
        
        progress.save()
        return progress

    @staticmethod
    def calculate_next_review(progress: Progress, rating: str) -> Dict:
        """
        Calculates next review date based on rating using hybrid SM2 algorithm
        
        Args:
            progress: Current Progress object
            rating: User rating ('again', 'hard', 'good', 'easy')
            
        Returns:
            Dictionary with updated progress values
        """
        # Rating to quality mapping
        ratings = {
            'again': 0,  # Complete blackout
            'hard': 2,   # Incorrect response
            'good': 3,   # Correct with difficulty
            'easy': 5    # Perfect response
        }
        
        quality = ratings.get(rating, 3)
        
        # Current values
        review_count = progress.review_count + 1
        correct_count = progress.correct_count + (1 if quality >= 3 else 0)
        ease_factor = progress.ease_factor or 2.5
        interval = progress.interval or 1
        
        # Hybrid approach: Fixed intervals for failed, SM2 for successful
        if quality < 3:
            # Failed cards - fixed short intervals
            if quality == 0:  # again
                interval = 10 / (24 * 60)  # 10 minutes
            else:  # hard
                interval = 15 / (24 * 60)  # 15 minutes
            
            ease_factor = max(1.3, ease_factor - 0.2)
        else:
            # Successful cards - adaptive SM2
            if review_count == 1:
                interval = 1  # 1 day
            elif review_count == 2:
                interval = 6  # 6 days
            else:
                multiplier = 1.3 if quality == 5 else 1.0
                interval = round(interval * ease_factor * multiplier)
            
            # Update ease factor
            ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        
        # Apply bounds
        ease_factor = max(1.3, min(ease_factor, 2.5))
        interval = max(10 / (24 * 60), min(interval, 365))
        
        # Calculate next review date
        interval_ms = interval * 24 * 60 * 60 * 1000
        next_review_date = datetime.utcnow() + timedelta(milliseconds=interval_ms)
        
        return {
            'review_count': review_count,
            'correct_count': correct_count,
            'ease_factor': round(ease_factor, 2),
            'interval': interval,
            'last_review_date': datetime.utcnow(),
            'next_review_date': next_review_date,
            'difficulty_rating': rating
        }

    @staticmethod
    def get_user_statistics(user_id: str) -> Dict:
        """
        Gets overall statistics for a user
        
        Args:
            user_id: The user ID
            
        Returns:
            Dictionary with user statistics
        """
        from app import db
        from app.models.deck import Deck
        
        # Get all flashcards for user
        flashcards = db.session.query(Flashcard)\
            .join(Deck)\
            .filter(Deck.user_id == user_id)\
            .all()
        
        total = len(flashcards)
        if total == 0:
            return {
                'total_flashcards': 0,
                'total_reviews': 0,
                'accuracy': 0.0,
                'due_today': 0,
                'mastered': 0,
                'learning': 0,
                'new': 0
            }
        
        total_reviews = 0
        total_correct = 0
        due_today = 0
        mastered = 0
        learning = 0
        new = 0
        now = datetime.utcnow()
        
        for flashcard in flashcards:
            if flashcard.progress:
                progress = flashcard.progress
                total_reviews += progress.review_count
                total_correct += progress.correct_count
                
                if progress.next_review_date <= now:
                    due_today += 1
                
                if progress.review_count == 0:
                    new += 1
                elif progress.review_count >= 5 and progress.ease_factor >= 2.5:
                    mastered += 1
                else:
                    learning += 1
        
        accuracy = (total_correct / total_reviews * 100) if total_reviews > 0 else 0.0
        
        return {
            'total_flashcards': total,
            'total_reviews': total_reviews,
            'accuracy': round(accuracy, 1),
            'due_today': due_today,
            'mastered': mastered,
            'learning': learning,
            'new': new
        }

    @staticmethod
    def reset_progress(flashcard_id: str) -> Optional[Progress]:
        """
        Resets progress for a flashcard to initial state
        
        Args:
            flashcard_id: The flashcard ID
            
        Returns:
            Reset Progress object or None if not found
        """
        progress = ProgressService.get_progress(flashcard_id)
        if not progress:
            return None
        
        progress.review_count = 0
        progress.correct_count = 0
        progress.ease_factor = 2.5
        progress.interval = 1
        progress.last_review_date = datetime.utcnow()
        progress.next_review_date = datetime.utcnow()
        progress.difficulty_rating = None
        
        progress.save()
        return progress
