from flask import Flask
from flask_migrate import Migrate


def init_app(app: Flask):
    from app.models.professionals_model import ProfessionalsModel 
    from app.models.patients_model import PatientModel
    from app.models.professionals_patients import professionals_patients
    from app.models.appointments_model import AppointmentsModel 

    Migrate(app, app.db)
