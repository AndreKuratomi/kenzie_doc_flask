from flask import Blueprint
from controllers.professionals_controller import (
    create_professional, get_all_professional,
    update_professional, delete_professional,
    get_all_specialty, get_one_specialty,
    get_health_plans
)

bp_professionals = Blueprint(
    'bp_professionals', __name__, url_prefix='/professionals')

bp_professionals.get('')(get_all_professional)
bp_professionals.post('')(create_professional)
bp_professionals.patch('/<int:id>')(update_professional)
bp_professionals.delete('/<int:id>')(delete_professional)
bp_professionals.get('/specialty')(get_all_specialty)
bp_professionals.get('/specialty/<str:specialty>')(get_one_specialty)
bp_professionals.get('/<int:id>/plans')(get_health_plans)
