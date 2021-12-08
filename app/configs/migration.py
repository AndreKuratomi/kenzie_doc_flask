from flask import Flask
from flask_migrate import Migrate


def init_app(app: Flask):
    from app.models.professionals_model import ProfessionalsModel
    from app.models.appointments_model import AppointmentsModel
    from app.models.professionals_patients import professionals_patients

    Migrate(app, app.db)
