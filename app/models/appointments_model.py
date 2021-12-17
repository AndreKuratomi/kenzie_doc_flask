from sqlalchemy.orm import relationship
from app.configs.database import db
from dataclasses import dataclass


@dataclass
class AppointmentsModel(db.Model):

    id: int
    patient_id: int
    professionals_id: str
    date: str
    complaint: str
    finished: str

    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(11), db.ForeignKey(
        "patients.cpf"), nullable=False)
    professionals_id = db.Column(
        db.String(20), db.ForeignKey("professionals.council_number"), nullable=False)
    date = db.Column(db.DateTime(), nullable=False, unique=True)
    complaint = db.Column(db.String, default="")
    finished = db.Column(db.Boolean, default=False)

    patient = db.relationship(
        'PatientModel', overlaps='appointments, appointments')
    professional = db.relationship('ProfessionalsModel')
