from flask import jsonify, request, current_app
from app.models.patients_model import PatientModel

#criar paciente
def create_pacient():
    data = request.json

    pacient = PatientModel(**data)

    current_app.db.session.add(pacient)
    current_app.db.session.commit()

    return jsonify(pacient), 201


#listar pacientes
def get_all_pacients():
    pacients = PatientModel.query.all()

    serializer = [
        {
        "age":pacient.age,
        "cpf":pacient.cpf,
        "email":pacient.email,
        "gender":pacient.gender,
        "health_insurance":pacient.health_insurance,
        "name": pacient.name,
        "password":pacient.password,
        "phone":pacient.phone
        }for pacient in pacients
    ]

    return jsonify(serializer), 200


#buscar um único paciente
def filter_by_pacient(cpf:str):
    pacients = PatientModel.query.filter_by(cpf=cpf)
    print(pacients)
    serializer = [
        {
        "age":pacient.age,
        "cpf":pacient.cpf,
        "email":pacient.email,
        "gender":pacient.gender,
        "health_insurance":pacient.health_insurance,
        "name": pacient.name,
        "password":pacient.password,
        "phone":pacient.phone
        }for pacient in pacients
    ]

    return jsonify(serializer), 200


#buscar por data
def get_by_date():
    ...


#atualizar paciente
def update_pacient(cpf:str):
    data = request.json

    pacient = PatientModel.query.filter_by(cpf=cpf).update(data)

    current_app.db.session.commit()

    update_pacient = PatientModel.query.get(cpf)

    return jsonify(update_pacient), 200


#deletar paciente
def delete_pacient(cpf:str):
    pacient = PatientModel.query.get(cpf)

    current_app.db.session.delete(pacient)
    current_app.db.session.commit()

    return jsonify(pacient), 200