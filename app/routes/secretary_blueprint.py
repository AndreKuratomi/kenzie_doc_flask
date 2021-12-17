from flask import Blueprint

from app.controllers.secretary_controller import create_secretary

bp_secretary = Blueprint(
    'bp_secretary', __name__, url_prefix='/secretary')

bp_secretary.post('')(create_secretary)