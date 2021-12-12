from app.configs.database import db
from dataclasses import dataclass
from app.models.professionals_patients import professionals_patients
from werkzeug.security import generate_password_hash, check_password_hash


@dataclass
class ProfessionalsModel(db.Model):

    council_number = str
    name: str
    email: str
    phone: str
    specialty: str
    address = str
    active: bool

    __tablename__ = 'professionals'

    council_number = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    specialty = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(50))
    password_hash = db.Column(db.String, nullable=True)
    active = db.Column(db.Boolean, default=True)

    patients = db.relationship("PatientModel", secondary=professionals_patients,
                               backref="professional_patients", uselist=True)

    @property
    def password(self):
        raise AttributeError("Password cannot be accessed!")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)
