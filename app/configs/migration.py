from flask import Flask
from flask_migrate import Migrate


def init_app(app: Flask):
    from app.models.professionals_model import ProfessionalsModel
    from app.models.patients_model import PatientModel
    from app.models.clinic_model import ClinicModel

    Migrate(app, app.db)
