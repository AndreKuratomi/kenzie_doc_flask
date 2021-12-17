from flask import jsonify, request, current_app
from app.models.patients_model import PatientModel
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from ipdb import set_trace
from sqlalchemy.orm.exc import UnmappedInstanceError
import re
from functools import wraps
from werkzeug.security import generate_password_hash
import os
from http import HTTPStatus


EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")


def create_patient():
    try:
        text_fields = ['cpf', 'name', 'email',
                       'phone', 'password', 'gender', 'health_insurance']

        required_keys = ['cpf', 'name', 'email',
                         'phone', 'password', 'age', 'gender', 'health_insurance']

        data = request.json
        
        # data["age"] = int(data["age"])
        print(data)
        print(data["age"])
        password_to_hash = data.pop("password")
        for key in data:
            if key != 'password' and key not in required_keys:
                raise KeyError

        if type(data['cpf']) != str or type(data['name']) != str or type(data['email']) != str or type(data['phone']) != str or type(data['gender']) != str or type(data['health_insurance']) != str:
            return {"msg": f"Numeric data is invalid. Text only fields: {text_fields}"}, 400

        if type(data['age']) != int:
            return {"error": "Invalid field 'age'. It must be an integer"}, 400

        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data['email']):
            return {"error": "Invalid email. Correct example yourname@provider.com"}, 400

        if not re.fullmatch(r"^(\([0-9]{2}\)[0-9]{5}-)[0-9]{4}$", data['phone']):
            return jsonify({"error": "Invalid phone number format. Correct example (xx)xxxxx-xxxx"}), 400

        if not re.fullmatch(r"^\d{3}\d{3}\d{3}\d{2}$", data['cpf']):
            return {"error": "Invalid field 'cpf'. Correct example: xxxxxxxxxxx"}, 400

        data['password'] = password_to_hash
        if type(data['password']) != str:
            return {"error": "Invalid field 'password'. It must be an string"}, 400

        patient = PatientModel(**data)

        current_app.db.session.add(patient)
        current_app.db.session.commit()
        return jsonify(patient), 201
    except IntegrityError:
        return {"error": "Patient already exists"}, 409

    except KeyError as e:
        return {"error": f"The key {e} is not valid"}, 400


@jwt_required()
def get_all_patients():
    current_user = get_jwt_identity()

    if current_user['email'] == EMAIL_ADDRESS:
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
        return jsonify(serializer), HTTPStatus.OK
    else:
        return jsonify({"message": "Unauthorized"}), HTTPStatus.UNAUTHORIZED


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
    current_user = get_jwt_identity()

    accepted_keys = ['name', 'email',
                     'health_insurance', 'age', 'phone', 'password']
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
            return jsonify({"error": "Invalid phone number format. Correct example (xx)xxxxx-xxxx"}), 400

    if age:
        data['age'] = age

    if 'password' in data:
        password_to_hash = data.pop("password")
        data['password_hash'] = generate_password_hash(password_to_hash)

    email_patient = PatientModel.query.get(cpf)

    if 'name' in data:
        data["name"] = data["name"].title()

    if 'health_insurance' in data:
        data["health_insurance"] = data["health_insurance"].title()

    try:
        if current_user['email'] == email_patient.email or current_user['email'] == EMAIL_ADDRESS:

            patient = PatientModel.query.filter_by(cpf=cpf).update(data)

            current_app.db.session.commit()

            update_patient = PatientModel.query.get(cpf)

            if update_patient:
                return jsonify(update_patient), 200
        return {"error": "No permission to update this patient"}, 403
    except (UnmappedInstanceError, AttributeError):
        return {"error": "Patient not found"}, 404


@jwt_required()
def delete_patient(cpf: str):
    current_user = get_jwt_identity()

    try:
        patient = PatientModel.query.get(cpf)

        if current_user['email'] == EMAIL_ADDRESS:
            current_app.db.session.delete(patient)
            current_app.db.session.commit()
            return {}, 204

        return {"error": "No permission to delete this patient"}, 403

    except (UnmappedInstanceError, AttributeError):
        return {"error": "Patient not found"}, 404
