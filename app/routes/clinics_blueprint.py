from flask import Blueprint
from app.controllers.clinics_controller import create_clinic, get_one_clinic,update_clinic, delete_clinic,get_clinic_professionals, get_clinic_accepted_plans, get_clinic_address
    

# bp_clinics = Blueprint(
#     'bp_clinics', __name__, url_prefix='/clinics')

# bp_clinics.get('/<int:id>')(get_one_clinic)
# bp_clinics.post('')(create_clinic)
# bp_clinics.patch('/<int:id>')(update_clinic)
# bp_clinics.delete('/<int:id>')(delete_clinic)
# bp_clinics.get('/professionals')(get_clinic_professionals)
# bp_clinics.get('/plans')(get_clinic_accepted_plans)
# bp_clinics.get('/address')(get_clinic_address)
