from flask import Blueprint
from controllers.appointments_controller import get_all_appointments, get_one_appointment

bp_appointments = Blueprint(
    'bp_appointments', __name__, url_prefix='/appointments')

bp_appointments.get('')(get_all_appointments)
bp_appointments.get('')(get_one_appointment)
bp_appointments.get('/<int: id>')('get_by_id')
bp_appointments.post('')('create_appointment')
