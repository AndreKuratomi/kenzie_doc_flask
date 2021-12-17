from app.configs.database import db
from dataclasses import dataclass

from werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class SecretaryModel(db.Model):
    name: str
    email: str
    phone: str

    __tablename__ = 'secretary'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=True)

    @property
    def password(self):
        raise AttributeError("Password cannot be accessed!")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)