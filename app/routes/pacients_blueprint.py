from flask import Blueprint
from controllers.pacients_controller import (
    create_pacients, update_pacients,
    delete_pacients, get_by_date
)

bp_pacients = Blueprint('bp_pacients', __name__, url_prefix='/pacients')

bp_pacients.post('')(create_pacients)
bp_pacients.patch('/<str:email>')(update_pacients)
bp_pacients.delete('/<str:email>')(delete_pacients)
# nao sei bem como fazer esse de pegar pela data
bp_pacients.get('/<date:date>')(get_by_date)
