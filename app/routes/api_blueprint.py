from flask import Blueprint
from . import professionals_blueprint, pacients_blueprint, appointments_blueprint


bp = Blueprint('api_bp', __name__, url_prefix='')

bp.register_blueprint(professionals_blueprint.bp_professionals)
bp.register_blueprint(pacients_blueprint.bp_pacients)
bp.register_blueprint(appointments_blueprint.bp_appointments)
