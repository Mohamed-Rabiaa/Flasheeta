#!/usr/bin/python3
""" Users API Endpoints """

from flask import Blueprint, jsonify
from app.services.user_service import UserService
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_view = Blueprint('users_view', __name__, url_prefix='/api/v1/') 

@users_view.route('/login', methods=['POST'], strict_slashes=False)
def login_user():
    """
    Logs in a user and returns a JWT token along with user data.

    Returns:
        tuple: A tuple containing a JSON response with the JWT token and user object, and HTTP status code 200.
    """
    from flask import request

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = UserService.authenticate_user(email, password)
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    
    # Return both token and user data for frontend
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@users_view.route('/users/me', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_current_user():
    """
    Retrieves the current authenticated user.

    Returns:
        tuple: A tuple containing a JSON response with the current user's information
               and an HTTP status code 200 if the user is authenticated, or a JSON
               response with an error message and HTTP status code 404 if the user
               is not found.
    """
    current_user_id = get_jwt_identity()
    
    from app.models.user import User    
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'error': 'Not Found'}), 404

    return jsonify(current_user.to_dict()), 200

@users_view.route('/register', methods=['POST'], strict_slashes=False)
def register_user():
    """
    Registers a new user and returns a JWT token along with user data.

    Returns:
        tuple: A tuple containing a JSON response with the JWT token and user object, and HTTP status code 201.
    """
    from flask import request

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Create new user using service layer
    new_user = UserService.create_user(username, email, password)
    
    # Generate JWT token for immediate login
    access_token = create_access_token(identity=new_user.id)
    
    return jsonify({
        'access_token': access_token,
        'user': new_user.to_dict()
    }), 201

@users_view.route('/logout', methods=['POST'], strict_slashes=False)
@jwt_required()
def logout_user():
    """
    Logs out the current user. 
    Note: For JWT, logout is handled client-side by deleting the token.
    This endpoint exists for API consistency.

    Returns:
        tuple: A tuple containing a JSON response with success message and HTTP status code 200.
    """
    return jsonify({'message': 'Successfully logged out'}), 200
