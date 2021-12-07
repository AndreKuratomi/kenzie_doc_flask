from app.configs.database import db
from dataclasses import dataclass


@dataclass
class AppointmentsModel(db.Model):

    id: int
    clinic_id: int
    pacient_id: str
    date: str
    finished: str

    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    finished = db.Column(db.Boolean, default=False)

    patient_id = db.Column(db.String(11), db.ForeignKey("patients.cpf"), nullable=False, unique=True)
    professionals_id = db.Column(db.String(20), db.ForeignKey("professionals.council_numbers"), nullable=False, unique=True)

    # clinic_id = db.Column(db.Integer,db.ForeignKey("clinics.id"))
