from flask import Blueprint
from app.controllers.login_controller import login_professional, login_patient


bp_login = Blueprint("bp_login", __name__, url_prefix='/login')


bp_login.post('/professional')(login_professional)
bp_login.post('/patient')(login_patient)
