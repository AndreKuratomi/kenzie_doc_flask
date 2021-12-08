from app.configs.database import db

professionals_patients = db.Table('professionals_patients',
    db.Column('id',db.Integer, primary_key=True),
    db.Column('patient_id',db.String(11), db.ForeignKey("patients.cpf"), nullable=False),
    db.Column('professionals_id', db.String(20), db.ForeignKey("professionals.council_numbers"), nullable=False),
)