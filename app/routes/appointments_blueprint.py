from flask import Blueprint
from app.controllers.appointment_controller import create_appointment, get_24h, get_by_pacient, get_by_professional, get_by_date, get_not_finished, update_appointment

bp_appointments = Blueprint(
    'bp_appointments', __name__, url_prefix='/appointments')

bp_appointments.post('')(create_appointment)
bp_appointments.get('/patient/<string:cpf>')(get_by_pacient)
bp_appointments.get(
    '/professional/<string:council_number>')(get_by_professional)
bp_appointments.get('/date/<string:date>')(get_by_date)
bp_appointments.get('/wait_list')(get_not_finished)
bp_appointments.patch('/<int:id>')(update_appointment)
bp_appointments.get('/tomorrow')(get_24h)
