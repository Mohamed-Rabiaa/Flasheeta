#!/usr/bin/python3
""" Users API Endpoints """

from flask import Blueprint, jsonify
from flask_login import current_user, login_required

users_view = Blueprint('users_view', __name__, url_prefix='/api/v1/') 

@users_view.route('/users/me', methods=['GET'], strict_slashes=False)
@login_required
def get_current_user():
    """
    Retrieves the current authenticated user.

    Returns:
        tuple: A tuple containing a JSON response with the current user's information
               and an HTTP status code 200 if the user is authenticated, or a JSON
               response with an error message and HTTP status code 404 if the user
               is not found.
    """
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
    from app.services.user_service import UserService

    new_user = UserService.create_user(user_name, email, password)
    return jsonify(new_user.to_dict()), 201
