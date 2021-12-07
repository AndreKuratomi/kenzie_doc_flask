from flask import Blueprint
from .professionals_blueprint import bp_professionals
from .pacients_blueprint import bp_pacients
from .appointments_blueprint import bp_appointments

bp = Blueprint('api_bp', __name__, url_prefix='/api')

bp.register_blueprint(bp_professionals)
bp.register_blueprint(bp_pacients)
bp.register_blueprint(bp_appointments)
