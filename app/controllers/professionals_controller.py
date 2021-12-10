from dataclasses import dataclass
from flask import jsonify, request, current_app
from app.models.professionals_model import ProfessionalsModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from psycopg2.errors import NotNullViolation
import re
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from ipdb import set_trace

# criar profissional
def create_professional():
    required_keys = ['council_number', 'name', 'email',
                     'phone', 'password', 'speciality', 'address']
    data = request.json

    data["council_number"] = data["council_number"].upper()
    data["name"] = data["name"].title()

    password_to_hash = data.pop("password")
    
    for key in data:
        if key not in required_keys:
            return {"msg": f"The key {key} is not valid"}, 400
        if type(data[key]) != str:
            return {"msg": "Fields must be strings"}, 422
        if key == 'speciality':
            value = data[key]
            data[key] = value.title()

    # set_trace()

    for key in required_keys:
        if key != 'password' and key not in data:
            return {"msg": f"Key {key} is missing"}, 400


    if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data['email']):
        return {"msg": "Invalid email"}, 400

    if not re.fullmatch(r'\(\d{2,}\)\d{4,}\-\d{4}', data['phone']):
        return {"msg": "Invalid phone number. Correct format: (xx)xxxxx-xxxx"}, 400

    if not re.fullmatch(r'[0-9]{3,5}-[A-Z]{2}', data['council_number']):
        return {"msg": "Invalid council number. Correct format: 00000-XX"}, 400

    try:
        data['password'] = password_to_hash
        new_professional = ProfessionalsModel(**data)
        # hash da senha
        current_app.db.session.add(new_professional)
        current_app.db.session.commit()
        return jsonify(new_professional), 201

    except IntegrityError:
        return {'msg': "User already exists"}, 409


# busca de todos od profissionais
def get_all_professionals():
    professionals = (ProfessionalsModel.query.all())
    result = [
        {
            "council_number": professional.council_number,
            "name": professional.name,
            "email": professional.email,
            "phone": professional.phone,
            "speciality": professional.speciality,
            "address": professional.address,
            "active": professional.active
        } for professional in professionals
    ]

    return jsonify(result), HTTPStatus.OK


# busca por uma especialidade especifica
def filter_by_speciality(speciality):
    title = speciality.title()
    professionals = (ProfessionalsModel.query.filter_by(speciality=title))

    result = [
        {
            "council_number": professional.council_number,
            "name": professional.name,
            "email": professional.email,
            "phone": professional.phone,
            "speciality": professional.speciality,
            "address": professional.address,
            "active": professional.active
        } for professional in professionals
    ]

    if len(result) < 1:
        return {"msg": f"No {speciality} found"}, 404

    return jsonify(result)


# atualiza os dados do profissional

@jwt_required()
def update_professional(cod):
    required_keys = ['council_number', 'name', 'email',
                     'phone', 'password', 'speciality', 'address']
    data = request.json
    for key in data:
        if key not in required_keys:
            return {"msg": f"The key {key} is not valid"}, 400
        if type(data[key]) != str:
            return {"msg": "Fields must be strings"}, 422
    crm = cod.upper()
    professional = ProfessionalsModel.query.filter_by(
        council_number=crm).update(data)
    current_app.db.session.commit()

    updated_professional = ProfessionalsModel.query.get(crm)

    if updated_professional:
        return jsonify(updated_professional), 200
    return {"msg": "Professional not found"}, 404


# deleta um profissional

@jwt_required()
def delete_professional(cod: str):
    
    try:
        professional = ProfessionalsModel.query.filter_by(council_number=cod.upper()).first()
        current_app.db.session.delete(professional)
        current_app.db.session.commit()
        return {} , 204
    except UnmappedInstanceError:
        return {"message": "Professional not found"} , 404


