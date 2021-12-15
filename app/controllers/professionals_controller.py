from dataclasses import dataclass
from flask import jsonify, request, current_app
from sqlalchemy.sql.elements import and_
from app.models.professionals_model import ProfessionalsModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
import re
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from ipdb import set_trace
from sqlalchemy import or_, and_
from werkzeug.security import generate_password_hash
import os

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")


def create_professional():
    required_keys = ['council_number', 'name', 'email',
                     'phone', 'password', 'speciality', 'address']
    data = request.json

    data["council_number"] = data["council_number"].upper()
    data["name"] = data["name"].title()
    data["speciality"] = data["speciality"].title()

    password_to_hash = data.pop("password")

    for key in data:
        if key not in required_keys:
            return {"error": f"The key {key} is not valid"}, 400
        if type(data[key]) != str:
            return {"error": "Fields must be strings"}, 422
        if key == 'speciality':
            value = data[key]
            data[key] = value.title()


    for key in required_keys:
        if key != 'password' and key not in data:
            return {"error": f"Key {key} is missing"}, 400

    if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data['email']):
        return {"error": "Invalid email"}, 400

    if not re.fullmatch(r'\(\d{2,}\)\d{4,}\-\d{4}', data['phone']):
        return {"error": "Invalid phone number. Correct format: (xx)xxxxx-xxxx"}, 400

    if not re.fullmatch(r'[0-9]{3,5}-[A-Z]{2}', data['council_number']):
        return {"error": "Invalid council number. Correct format: 00000-XX"}, 400

    try:
        data['password'] = password_to_hash
        new_professional = ProfessionalsModel(**data)
        current_app.db.session.add(new_professional)
        current_app.db.session.commit()
        return jsonify(new_professional), 201

    except IntegrityError:
        return {'error': "User already exists"}, 409


@jwt_required()
def get_all_professionals():
    current_user = get_jwt_identity()
    if current_user['email'] == EMAIL_ADDRESS:
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
    else:
        return jsonify({"message": "Unauthorized"}), HTTPStatus.UNAUTHORIZED


def filter_by_speciality():
    speciality = request.args.get("speciality", default=None)
    name = request.args.get("name", default=None)
    address = request.args.get("address", default=None)

    if speciality:
        speciality = speciality.title()
    if name:
        name = name.title()
    if address:
        address = address.title()

    professionals = ProfessionalsModel.query.filter(
        or_(ProfessionalsModel.speciality == speciality, ProfessionalsModel.name.like(f'%{name}%'), ProfessionalsModel.address.like(f'%{address}%')))

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
        return {"error": f"No {speciality} found"}, 404

    return jsonify(result)


@jwt_required()
def update_professional(cod):
    current_user = get_jwt_identity()

    required_keys = ['council_number', 'name', 'email',
                     'phone', 'password', 'speciality', 'address']
    
    data = request.json

    for key in data:
        if key not in required_keys:
            return {"error": f"The key {key} is not valid"}, 400
        if type(data[key]) != str:
            return {"error": "Fields must be strings"}, 422
            
    crm = cod.upper()

    if 'speciality' in data:
        data["speciality"] = data["speciality"].title()

    if 'name' in data:
        data["name"] = data["name"].title()
    
    if 'password' in data:
        password_to_hash = data.pop("password")
        data['password_hash'] = generate_password_hash(password_to_hash)

    email_professional = ProfessionalsModel.query.get(crm)

    try:
        if current_user['email'] == email_professional.email or current_user['email'] == EMAIL_ADDRESS:

            professional = ProfessionalsModel.query.filter_by(
            council_number=crm).update(data)

            current_app.db.session.commit()

            updated_professional = ProfessionalsModel.query.get(crm)

            if updated_professional:
                return jsonify(updated_professional), 200
        else:
            return jsonify({"message": "No permission to update this professional"}), HTTPStatus.UNAUTHORIZED

        return {"error": "No permission to update this professional"}, 403

    except (UnmappedInstanceError, AttributeError):
        return {"error": "Professional not found"}, 404


@jwt_required()
def delete_professional(cod: str):
    current_user = get_jwt_identity()

    try:       

        professional = ProfessionalsModel.query.filter_by(
            council_number=cod.upper()).first()
        
            
        if current_user['email'] == EMAIL_ADDRESS:
            current_app.db.session.delete(professional)
            current_app.db.session.commit()
            return {}, 204

        return {"msg": "No permission to delete this professional"}, 403
        
    except (UnmappedInstanceError, AttributeError):
        return {"error": "Professional not found"} , 404


