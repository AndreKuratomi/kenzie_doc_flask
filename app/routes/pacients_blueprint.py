from flask import Blueprint
from controllers.pacients_controller import (
    create_pacients, get_all_pacients,
    update_pacients, delete_pacients,
    get_one_pacient
)

bp_pacients = Blueprint('bp_pacients', __name__, url_prefix='/pacients')

bp_pacients.get('')(get_all_pacients)
bp_pacients.get('/<int:id>')(get_one_pacient)
bp_pacients.post('')(create_pacients)
bp_pacients.patch('/<str:email>')(update_pacients)
bp_pacients.delete('/<str:email>')(delete_pacients)
