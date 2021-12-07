from flask import jsonify, request, current_app
from app.models.patients_model import PatientModel
from sqlalchemy.exc import IntegrityError
import re

#criar paciente
def create_pacient():
    required_keys = ['cpf', 'name', 'email',
                     'phone', 'password', 'age', 'gender', 'health_insurance']
    data = request.json

    for key in data:
        if key not in required_keys:
            return {"msg": f"The key {key} is not valid"}, 400

    if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data['email']):
        return {"msg": "Invalid email. Correct example yourname@provider.com"}, 400

    if not re.fullmatch(r'\(\d{2,}\)\d{4,}\-\d{4}', data['phone']):
        return {"msg": "Invalid phone number"}, 400 
    
    validate_phone = re.fullmatch(r"^(\([0-9]{2}\)[0-9]{5}-)[0-9]{4}$", data['phone'])
    if validate_phone == None:
        return jsonify({"error": "Invalid phone number format. Correct example (xx)xxxxx-xxxx"})

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