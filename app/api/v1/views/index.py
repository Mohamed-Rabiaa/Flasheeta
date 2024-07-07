#!/usr/bin/python3
""" Index API Endpoint """

from flask import jsonify, Blueprint

index_view = Blueprint('index_view', __name__, url_prefix='/api/v1')

@index_view.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Returns the status of the API.

    Returns:
        tuple: A tuple containing a JSON response with the status message "OK" and an HTTP status code 200.
    """
    return jsonify({"status": "OK"})
