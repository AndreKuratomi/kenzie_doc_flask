from app.configs.database import db
from dataclasses import dataclass
from app.models.professionals_patients import professionals_patients
from werkzeug.security import generate_password_hash, check_password_hash


@dataclass
class PatientModel(db.Model):
    cpf: str
    age: int
    gender: str
    email: str
    name: str
    # password: str
    phone: str
    health_insurance: str

    __tablename__ = "patients"

    cpf = db.Column(db.String(11), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    email = db.Column(db.String(50), nullable=False, unique=True)
    # password = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20))
    health_insurance = db.Column(db.String(50))
    password_hash = db.Column(db.String, nullable=True)

    appointments = db.relationship("AppointmentsModel", backref="appointments", uselist=True)


    @property
    def password(self):
        raise AttributeError("Password cannot be accessed!")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)
