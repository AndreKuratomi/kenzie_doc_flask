from flask import jsonify, request, current_app
from app.models.appointments_model import AppointmentsModel
from app.models.patients_model import PatientModel
from sqlalchemy.exc import IntegrityError
import re

# criar patiente
def create_patient():
    try:
        text_fields = ['cpf', 'name', 'email',
                        'phone', 'password', 'gender', 'health_insurance']
                        
        required_keys = ['cpf', 'name', 'email',
                        'phone', 'password', 'age', 'gender', 'health_insurance']

        data = request.json

        for key in data:
            #print(key, "**************")
            if key not in required_keys:
                print(key)
                raise KeyError

        if type(data['cpf']) != str or type(data['name']) != str or type(data['email']) != str or type(data['phone']) != str or type(data['password']) != str or type(data['gender']) != str or type(data['health_insurance']) != str:
                return {"msg": f"Numeric data is invalid. Text only fields: {text_fields}"}, 400
        
        if type(data['age']) != int:
            return {"msg": "Invalid field age."} , 400

        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data['email']):
            return {"msg": "Invalid email. Correct example yourname@provider.com"}, 400
    
        if not re.fullmatch(r"^(\([0-9]{2}\)[0-9]{5}-)[0-9]{4}$", data['phone']):
            return jsonify({"error": "Invalid phone number format. Correct example (xx)xxxxx-xxxx"})
        
        if not re.fullmatch(r"^\d{3}\d{3}\d{3}\d{2}$", data['cpf']):
            return {"msg": "Invalid field 'cpf'. Correct example: xxxxxxxxxxx"} , 400

        patient = PatientModel(**data)

        current_app.db.session.add(patient)
        current_app.db.session.commit()

        return jsonify(patient), 201

    except IntegrityError:
        return {"msg": "Patient already exists"} , 409
    except KeyError as e:
        return {"msg": f"The key {e} is not valid"}, 400


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

    required_keys = ['cpf', 'name', 'email',
                    'phone', 'password', 'age', 'gender', 'health_insurance']
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


# deletar patiente
def delete_patient(cpf: str):
    patient = PatientModel.query.get(cpf)

    current_app.db.session.delete(patient)
    current_app.db.session.commit()

    return jsonify(patient)
