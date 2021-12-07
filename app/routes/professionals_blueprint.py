from flask import Blueprint
from app.controllers.professionals_controller import (
    create_professional, update_professional, delete_professional,
    get_by_clinic, filter_by_specialty
)

bp_professionals = Blueprint(
    'bp_professionals', __name__, url_prefix='/professionals')

bp_professionals.post('')(create_professional)
bp_professionals.patch('/<id>')(update_professional)
bp_professionals.delete('/<id>')(delete_professional)
bp_professionals.get('/clinic/<id>')(get_by_clinic)
bp_professionals.get('/<specialty>')(filter_by_specialty)
