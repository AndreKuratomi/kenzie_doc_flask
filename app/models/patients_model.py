from app.configs.database import db
from dataclasses import dataclass


@dataclass
class PatientModel(db.Model):
    cpf: str
    age: int
    gender: str
    email: str
    name: str
    password: str
    phone: str
    health_insurance: str

    __tablename__ = "patients"

    cpf = db.Column(db.String(11), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20))
    health_insurance = db.Column(db.String(50))

    appointments = db.relationship("AppointmentsModel", backref="appointments", uselist=True)
