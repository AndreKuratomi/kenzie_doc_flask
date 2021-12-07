from app.configs.database import db

appointment_table = db.Table('appointment',
    db.Column('id',db.Integer, primary_key=True),
    # db.Column('date',db.DateTime, nullable=False),
    # db.Column('finished',db.Boolean, default=False),
    db.Column('patient_id',db.String(11), db.ForeignKey("patients.cpf"), nullable=False, unique=True),
    db.Column('professionals_id', db.String(20), db.ForeignKey("professionals.council_numbers"), nullable=False, unique=True),
    
)