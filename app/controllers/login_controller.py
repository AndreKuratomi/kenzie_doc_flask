from flask import Blueprint, request
from http import HTTPStatus
from app.models.professionals_model import ProfessionalsModel
from app.models.patients_model import PatientModel
from flask_jwt_extended import create_access_token


def login_professional():
    user_data = request.get_json()

    found_user: ProfessionalsModel = ProfessionalsModel.query.filter_by(email=user_data["email"]).first()

    if not found_user:
        return {"message": "User not found"}, HTTPStatus.NOT_FOUND

    if found_user.verify_password(user_data["password"]):
        access_token = create_access_token(identity=found_user)
        return {"message": access_token}, HTTPStatus.OK
    else:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED


def login_patient():
    user_data = request.get_json()

    found_user: PatientModel = PatientModel.query.filter_by(email=user_data["email"]).first()

    if not found_user:
        return {"message": "User not found"}, HTTPStatus.NOT_FOUND

    if found_user.verify_password(user_data["password"]):
        access_token = create_access_token(identity=found_user)
        return {"message": access_token}, HTTPStatus.OK
    else:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED