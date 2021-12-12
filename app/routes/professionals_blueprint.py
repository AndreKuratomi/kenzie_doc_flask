from flask import Blueprint
from app.controllers.professionals_controller import create_professional, update_professional, delete_professional,get_all_professionals, filter_by_specialty


bp_professionals = Blueprint(
    'bp_professionals', __name__, url_prefix='/professionals')

bp_professionals.post('')(create_professional)
bp_professionals.get('')(get_all_professionals)
bp_professionals.get('/<string:speciality>')(filter_by_specialty)
bp_professionals.patch('/<string:cod>')(update_professional)
bp_professionals.delete('/<string:cod>')(delete_professional)
