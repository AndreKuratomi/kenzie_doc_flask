from flask import jsonify, request, current_app
from app.models.patients_model import PatientModel
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required
from ipdb import set_trace
import re

def create_patient():
    try:
        text_fields = ['cpf', 'name', 'email',
                       'phone', 'password', 'gender', 'health_insurance']

        required_keys = ['cpf', 'name', 'email',
                         'phone', 'password', 'age', 'gender', 'health_insurance']

        data = request.json

        password_to_hash = data.pop("password")

        for key in data:
            print(key, "**************")
            if key != 'password' and key not in required_keys:
                print(key)
                raise KeyError

        # keila: tirei o type(data['password]) da verificação abaixo
        # or type(data['password']) != str
        if type(data['cpf']) != str or type(data['name']) != str or type(data['email']) != str or type(data['phone']) != str or type(data['gender']) != str or type(data['health_insurance']) != str:
            return {"msg": f"Numeric data is invalid. Text only fields: {text_fields}"}, 400

        if type(data['age']) != int:
            return {"error": "Invalid field 'age'. It must be an integer"} , 400

        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data['email']):
            return {"error": "Invalid email. Correct example yourname@provider.com"}, 400

        if not re.fullmatch(r"^(\([0-9]{2}\)[0-9]{5}-)[0-9]{4}$", data['phone']):
            return jsonify({"error": "Invalid phone number format. Correct example (xx)xxxxx-xxxx"}) , 400

        if not re.fullmatch(r"^\d{3}\d{3}\d{3}\d{2}$", data['cpf']):
            return {"error": "Invalid field 'cpf'. Correct example: xxxxxxxxxxx"} , 400

        data['password'] = password_to_hash

        if type(data['password']) != str:
            return {"error": "Invalid field 'password'. It must be an string"}, 400

        patient = PatientModel(**data)

        current_app.db.session.add(patient)
        current_app.db.session.commit()
        return jsonify(patient), 201

    except IntegrityError:
        return {"error": "Patient already exists"} , 409

    except KeyError as e:
        return {"error": f"The key {e} is not valid"}, 400


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
            "phone": patient.phone
        } for patient in patients
    ]

    return jsonify(serializer), 200


def filter_by_patient(cpf: str):

    patient_found = PatientModel.query.filter_by(cpf=cpf)

    serializer = [
        {
            "age": patient.age,
            "cpf": patient.cpf,
            "email": patient.email,
            "gender": patient.gender,
            "health_insurance": patient.health_insurance,
            "name": patient.name,
            "phone": patient.phone

        } for patient in patient_found
    ]

    if len(serializer) != 0:
        return jsonify(serializer), 200

    return {"error": "Patient not found"}, 404


@jwt_required()
def update_patient(cpf: str):
    accepted_keys = ['name', 'email', 'health_insurance', 'age', 'phone']
    age = None
    data = request.json

    if 'age' in data:
        age = data.pop('age')
        if type(age) != int:
            return {"error": "Invalid field 'age'. It must be an integer."}, 400

    for key in data:
        if key not in accepted_keys:
            return {"error": f"The key {key} is not valid"}, 400
        if type(data[key]) != str:
            return {"error": "Numeric data is invalid. Text field only"}, 400
    if 'email' in data:
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data['email']):
            return {"error": "Invalid email . Correct example yourname@provider.com"}, 400
    if 'phone' in data:
        if not re.fullmatch(r"^(\([0-9]{2}\)[0-9]{5}-)[0-9]{4}$", data['phone']):
            return jsonify({"error": "Invalid phone number format. Correct example (xx)xxxxx-xxxx"}) , 400

    if age:
        data['age'] = age

    patient = PatientModel.query.filter_by(cpf=cpf).update(data)

    current_app.db.session.commit()

    update_patient = PatientModel.query.get(cpf)

    if update_patient:
        return jsonify(update_patient), 200
    return {"msg": "Patient not found"}, 404


@jwt_required()
def delete_patient(cpf: str):
    try:
        patient = PatientModel.query.get(cpf)

        current_app.db.session.delete(patient)
        current_app.db.session.commit()

        return "", 204

    except:
        return {"msg": "Patient not found"}, 404
