from flask import Blueprint
from app.controllers.pacients_controller import create_pacient, update_pacient, delete_pacient, get_by_date, filter_by_pacient, get_all_pacients


bp_pacients = Blueprint('bp_pacients', __name__, url_prefix='/pacients')

bp_pacients.post('')(create_pacient)
bp_pacients.patch('/<string:cpf>')(update_pacient)
bp_pacients.delete('/<string:cpf>')(delete_pacient)
# nao sei bem como fazer esse de pegar pela data
bp_pacients.get('')(get_all_pacients)
bp_pacients.get('/<string:cpf>')(filter_by_pacient)
bp_pacients.get('/<int:id>')(get_by_date)
