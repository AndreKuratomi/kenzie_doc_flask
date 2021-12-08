from flask import jsonify, request, current_app
from app.models.patients_model import PatientModel

# criar patiente


def create_patient():
    data = request.json

    patient = PatientModel(**data)

    current_app.db.session.add(patient)
    current_app.db.session.commit()

    return jsonify(patient), 201


# listar patientes
def get_all_patients():
    patients = PatientModel.query.all()

    serializer = [
        {
            "age": patient.age,
            "cpf": patient.cpf,
            "email": patient.email,
            "gender": patient.gender,
            "health_insurance": patient.health_insurance,
            "name": patient.name,
            "password": patient.password,
            "phone": patient.phone
        }for patient in patients
    ]

    return jsonify(serializer), 200


# buscar um único patiente
def filter_by_patient(cpf: str):
    patients = PatientModel.query.filter_by(cpf=cpf)
    print(patients)
    serializer = [
        {
            "age": patient.age,
            "cpf": patient.cpf,
            "email": patient.email,
            "gender": patient.gender,
            "health_insurance": patient.health_insurance,
            "name": patient.name,
            "password": patient.password,
            "phone": patient.phone
        }for patient in patients
    ]

    return jsonify(serializer), 200


# buscar por data
def get_by_date():
    ...


# atualizar patiente
def update_patient(cpf: str):
    data = request.json

    patient = PatientModel.query.filter_by(cpf=cpf).update(data)

    current_app.db.session.commit()

    update_patient = PatientModel.query.get(cpf)

    return jsonify(update_patient), 200


# deletar patiente
def delete_patient(cpf: str):
    patient = PatientModel.query.get(cpf)

    current_app.db.session.delete(patient)
    current_app.db.session.commit()

    return jsonify(patient), 200
