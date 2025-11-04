#!/usr/bin/python3
"""
Deck Service Layer
Handles business logic for deck operations
"""

from typing import List, Optional, Dict
from app.models.deck import Deck
from app.models.user import User
from app.exceptions import ValidationError, NotFoundError, ConflictError
from flask import current_app as app


class DeckService:
    """Service class for deck-related operations"""

    @staticmethod
    def create_deck(name: str, user_id: str) -> Deck:
        """
        Creates a new deck for a user
        
        Args:
            name: The deck name
            user_id: The ID of the user who owns the deck
            
        Returns:
            The created Deck object
            
        Raises:
            ValueError: If name is empty or deck name already exists for user
        """
        # Validate name
        if not name or not name.strip():
            raise ValidationError("Deck name cannot be empty")
        
        # Check if deck with same name already exists for this user
        existing_deck = Deck.query.filter_by(
            name=name.strip(),
            user_id=user_id
        ).first()
        
        if existing_deck:
            raise ConflictError(f"Deck with name '{name}' already exists")
        
        # Create deck
        deck = Deck(name=name.strip(), user_id=user_id)
        deck.save()
        
        return deck

    @staticmethod
    def get_deck_by_id(deck_id: str) -> Optional[Deck]:
        """
        Retrieves a deck by its ID
        
        Args:
            deck_id: The deck ID
            
        Returns:
            Deck object or None if not found
        """
        return app.storage.get(Deck, deck_id)

    @staticmethod
    def get_decks_by_user(user_id: str, order_by: str = 'name') -> List[Deck]:
        """
        Retrieves all decks for a specific user
        
        Args:
            user_id: The user ID
            order_by: Field to order by ('name', 'created_at', 'updated_at')
            
        Returns:
            List of Deck objects
        """
        query = Deck.query.filter_by(user_id=user_id)
        
        if order_by == 'name':
            query = query.order_by(Deck.name)
        elif order_by == 'created_at':
            query = query.order_by(Deck.created_at.desc())
        elif order_by == 'updated_at':
            query = query.order_by(Deck.updated_at.desc())
        
        return query.all()

    @staticmethod
    def update_deck(deck_id: str, name: Optional[str] = None) -> Optional[Deck]:
        """
        Updates a deck's name
        
        Args:
            deck_id: The deck ID
            name: New deck name
            
        Returns:
            Updated Deck object or None if not found
            
        Raises:
            ValueError: If name is empty or already exists
        """
        deck = app.storage.get(Deck, deck_id)
        if not deck:
            return None
        
        if name is not None:
            if not name.strip():
                raise ValueError("Deck name cannot be empty")
            
            # Check if another deck with same name exists for this user
            existing_deck = Deck.query.filter_by(
                name=name.strip(),
                user_id=deck.user_id
            ).first()
            
            if existing_deck and existing_deck.id != deck_id:
                raise ValueError(f"Deck with name '{name}' already exists")
            
            deck.name = name.strip()
        
        deck.save()
        return deck

    @staticmethod
    def delete_deck(deck_id: str) -> bool:
        """
        Deletes a deck and all its flashcards
        
        Args:
            deck_id: The deck ID
            
        Returns:
            True if deleted, False if not found
        """
        deck = app.storage.get(Deck, deck_id)
        if not deck:
            return False
        
        # Delete all flashcards in the deck (cascade should handle this)
        # But being explicit for clarity
        for flashcard in deck.flashcards:
            if flashcard.progress:
                app.storage.delete(flashcard.progress)
            app.storage.delete(flashcard)
        
        app.storage.delete(deck)
        app.storage.save()
        return True

    @staticmethod
    def get_deck_with_statistics(deck_id: str) -> Optional[Dict]:
        """
        Gets a deck with its statistics
        
        Args:
            deck_id: The deck ID
            
        Returns:
            Dictionary with deck data and statistics, or None if not found
        """
        deck = app.storage.get(Deck, deck_id)
        if not deck:
            return None
        
        result = deck.to_dict()
        
        # Get statistics
        from app.services.flashcard_service import FlashcardService
        stats = FlashcardService.get_statistics(deck_id)
        result['statistics'] = stats
        
        return result

    @staticmethod
    def verify_deck_ownership(deck_id: str, user_id: str) -> bool:
        """
        Verifies that a deck belongs to a specific user
        
        Args:
            deck_id: The deck ID
            user_id: The user ID
            
        Returns:
            True if user owns the deck, False otherwise
        """
        deck = app.storage.get(Deck, deck_id)
        if not deck:
            return False
        
        return deck.user_id == user_id

    @staticmethod
    def get_user_deck_count(user_id: str) -> int:
        """
        Gets the number of decks a user has
        
        Args:
            user_id: The user ID
            
        Returns:
            Number of decks
        """
        return Deck.query.filter_by(user_id=user_id).count()
