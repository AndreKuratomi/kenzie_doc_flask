from app.configs.database import db
from dataclasses import dataclass
# from sqlalchemy.orm import relationship
from app.models.professionals_patients import professionals_patients

@dataclass
class ProfessionalsModel(db.Model):

    council_number = str
    name: str
    email: str
    phone: str
    password: str
    specialty: str
    address = str

    __tablename__ = 'professionals'

    council_number = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(20), nullable=False)
    specialty = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(50))

    patients = db.relationship("PatientModel", secondary=professionals_patients,backref="professional_patients", uselist=True)

    # clinic = relationship("Clinics", backref="professional")

    # @validates()
