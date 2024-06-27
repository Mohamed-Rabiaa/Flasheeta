#!/usr/bin/python3
""" Users """


from flask import Blueprint, jsonify
from flask_login import current_user

users_view = Blueprint('users_view', __name__, url_prefix='/api/v1/') 


@users_view.route('/users/me', methods=['GET'], strict_slashes=False)
def get_current_user():
    """
    Retrieves the current user 
    """
    if not current_user:
        return jsonify({'error': 'Not Found'}), 404

    return jsonify(current_user.to_dict()), 200
