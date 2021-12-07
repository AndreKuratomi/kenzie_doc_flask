from flask import Blueprint
from app.controllers.appointment_controller import get_by_pacient, get_by_professional, get_by_date, get_not_finished

bp_appointments = Blueprint(
    'bp_appointments', __name__, url_prefix='/appointments')

bp_appointments.get('/<string:cpf>')(get_by_pacient)
bp_appointments.get('/<string:council_number>')(get_by_professional)
bp_appointments.get('/<int:id>')(get_by_date)
bp_appointments.post('/wait_list')(get_not_finished)
