from app.configs.database import db
from dataclasses import dataclass

@dataclass
class ClinicModel(db.Model):
    id: int
    professionals: str
    email: str
    phone: str
    password: str
    accepted_plans: str

    id = db.Column(db.Integer, primary_key=True)
    # professionals = ForeignKey
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(20)) 
    password = db.Column(db.String(20), nullable=False)
    accepted_plans = db.Column(db.String(50))
    address = db.Column(db.String(50))
