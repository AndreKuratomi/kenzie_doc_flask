from app.configs.database import db
from dataclasses import dataclass

@dataclass
class AppointmentsModel(db.Model):

    id = int
    clinic_id: int
    pacient_id: str
    date: str
    finished: str

    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer,db.ForeignKey("clinics.id"))
    pacient_id = db.Column(db.String(20), db.ForeignKey("patients.cpf"))
    date = db.Column(db.DateTime, nullable=False)
    finished = db.Column(db.Boolean, default=False)

