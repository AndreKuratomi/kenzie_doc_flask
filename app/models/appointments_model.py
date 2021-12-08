from sqlalchemy.orm import relationship
from app.configs.database import db
from dataclasses import dataclass

@dataclass
class AppointmentsModel(db.Model):

    id: int
    patient_id: int
    professionals_id: str
    date: str
    finished: str

    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(11), db.ForeignKey("patients.cpf"), unique=True)
    professionals_id = db.Column(db.String(20), db.ForeignKey("professionals.council_numbers"), unique=True)
    date = db.Column(db.DateTime(), nullable=False)
    finished = db.Column(db.Boolean, default=False)
     # clinic_id = db.Column(db.Integer,db.ForeignKey("clinics.id")) 

    patient = relationship('PatientModel')
