#!/usr/bin/python3
""" Users API Endpoints """

from flask import Blueprint, jsonify
from app.services.user_service import UserService
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_view = Blueprint('users_view', __name__, url_prefix='/api/v1/') 

@users_view.route('/login', methods=['POST'], strict_slashes=False)
def login_user():
    """
    Logs in a user and returns a JWT token.

    Returns:
        tuple: A tuple containing a JSON response with the JWT token and an HTTP status code 200.
    """
    from flask import request

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = UserService.authenticate_user(email, password)
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

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

@users_view.route('/users', methods=['POST'], strict_slashes=False)
def create_user(user_name, email, password):
    """
    Creates a new user.

    Args:
        user_name (str): The username for the new user.
        email (str): The email address for the new user.
        password (str): The password for the new user.
    Returns:
        tuple: A tuple containing a JSON response with the newly created user's information
               and an HTTP status code 201.
    """
    new_user = UserService.create_user(user_name, email, password)
    return jsonify(new_user.to_dict()), 201
