#!/usr/bin/python3
""" Index """


from flask import jsonify, Blueprint

index_view = Blueprint('index_view', __name__, url_prefix='/api/v1')

@index_view.route('/status', methods=['GET'],
                 strict_slashes=False)
def status():
    """ Return the status of this API """
    return jsonify({"status":"OK"})
