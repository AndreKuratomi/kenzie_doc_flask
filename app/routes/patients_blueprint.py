from flask import Blueprint
from app.controllers.patients_controller import create_patient, update_patient, delete_patient, filter_by_patient, get_all_patients


bp_patients = Blueprint('bp_patients', __name__, url_prefix='/patients')

bp_patients.post('')(create_patient)
bp_patients.get('')(get_all_patients)
bp_patients.get('/<string:cpf>')(filter_by_patient)
bp_patients.patch('/<string:cpf>')(update_patient)
bp_patients.delete('/<string:cpf>')(delete_patient)
