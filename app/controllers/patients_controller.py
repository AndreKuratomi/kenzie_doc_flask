from flask import jsonify, request, current_app
from app.models.appointments_model import AppointmentsModel
from app.models.patients_model import PatientModel
from sqlalchemy.exc import IntegrityError
import re
from ipdb import set_trace

required_keys = ['cpf', 'name', 'email', 'phone', 'password', 'age', 'gender', 'health_insurance']


def create_patient():
    try:
        data = request.get_json()

        keys = data.keys()
        set_keys = set(keys)
        set_required_keys = set(required_keys)
        diff = set_required_keys.difference(set_keys)

        if diff != set():
            if len(diff) == 1:
                return {"error": f"The key {diff} is not present."}, 400
            else:
                return {"error": f"The keys {diff} are not present."}, 400

        if type(data['cpf']) != str or type(data['name']) != str or type(data['email']) != str or type(data['phone']) != str or type(data['password']) != str or type(data['gender']) != str or type(data['health_insurance']) != str:
            return {"error": "Invalid type data. Fields other than 'age' must be only strings"}, 400
        
        if type(data['age']) != int:
            return {"error": "Invalid field 'age'. It must be an integer"}

        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data['email']):
            return {"error": "Invalid email. Correct example yourname@provider.com"}, 400

        if not re.fullmatch(r'\d{3}\.\d{3}\.\d{3}\-\d{2}', data['cpf']):
            return {"error": "Invalid CPF format. Correct example: xxx.xxx.xxx-xx"}, 400 
        
        validate_phone = re.fullmatch(r"^(\([0-9]{2}\)[0-9]{5}-)[0-9]{4}$", data['phone'])
        if validate_phone == None:
            return {"error": "Invalid phone number format. Correct example: (xx)yxxxx-xxxx"}, 400

        patient = PatientModel(**data)

        current_app.db.session.add(patient)
        current_app.db.session.commit()

        return jsonify(patient), 201

    except IntegrityError:
        return {"msg": "Patient already exists. Please check CPF and email."}, 409


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
        }   for patient in patients
    ]

    return jsonify(serializer), 200


def filter_by_patient(cpf: str):

    patients = PatientModel.query.filter_by(cpf=cpf)

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
        }   for patient in patients
    ]

    return jsonify(serializer), 200


def get_by_date():
    ...


def update_patient(cpf: str):

    age = None
    data = request.json

    if 'age' in data:
        age = data.pop('age')
        if type(age) != int:
            return {"msg": "Invalid field age. "}, 400

    for key in data:
        if key not in required_keys:
            return {"msg": f"The key {key} is not valid"}, 400
        if type(data[key]) != str:
            return {"msg": "Numeric data is invalid. Text field only"}, 400

    if age: 
        data['age'] = age

    patient = PatientModel.query.filter_by(cpf=cpf).update(data)

    current_app.db.session.commit()

    update_patient = PatientModel.query.get(cpf)

    if update_patient:
        return jsonify(update_patient), 200
    return {"msg": "Patient not found"}, 404



def delete_patient(cpf: str):

    patient = PatientModel.query.get(cpf)

    current_app.db.session.delete(patient)
    current_app.db.session.commit()

    return jsonify(patient)
