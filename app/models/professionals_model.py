from app.configs.database import db
from dataclasses import dataclass
# from sqlalchemy.orm import relationship

@dataclass
class ProfessionalsModel(db.Model):

   # council_number = str
   # name: str
   # email: str
   # phone: str
   # password: str
   # specialty: str
   # address = str

    __tablename__ = 'professionals'

    council_numbers = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(20), nullable=False)
    specialty = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(50))

    #appointments = db.relationship("AppointmentsModel", backref="professionals_appointments", uselist=True)
    # clinic = relationship("Clinics", backref="professional")

    # @validates()
