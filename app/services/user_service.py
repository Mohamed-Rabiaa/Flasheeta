#!/usr/bin/python3
""" User Service Module
Handles business logic for user operations
"""
from app.models.user import User
from app.exceptions import ValidationError
from werkzeug.security import generate_password_hash

class UserService:
    """Service class for user-related operations"""
    @staticmethod
    def create_user(username: str, email: str, password: str):
        """
        Creates a new user
        
        Args:
            username: The user's username
            email: The user's email
            password: The user's password
            
        Returns:
            The created User object
            
        Raises:
            ValueError: If any input is invalid
        """
        # Validate inputs
        if not username or not username.strip():
            raise ValidationError("Username cannot be empty")
        if not email or not email.strip():
            raise ValidationError("Email cannot be empty")
        if not password or not password.strip():
            raise ValidationError("Password cannot be empty")
        
        # Hash password (business logic in service layer)
        password_hash = generate_password_hash(password)
        
        # Create user
        user = User(
            username=username.strip(),
            email=email.strip(),
            password_hash=password_hash
        )
        user.save()
        
        return user
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> User:
        """
        Authenticates a user by email and password
        
        Args:
            email: The user's email
            password: The user's password
            
        Returns:
            The authenticated User object
            
        Raises:
            ValidationError: If authentication fails
        """
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            raise ValidationError("Invalid email or password")
        
        return user
        