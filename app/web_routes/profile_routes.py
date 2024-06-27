#!/usr/bin/python3
""" profile_route module """



from flask import current_app as app, Blueprint, render_template
from flask_login import login_required
from app.models.user import User

bp = Blueprint('profile', __name__)


@bp.route('/users/<user_id>/profile', methods=['GET'],
         strict_slashes=False)
@login_required
def profile(user_id):
    """ Displays the profile page """    
    return render_template('profile.html')
