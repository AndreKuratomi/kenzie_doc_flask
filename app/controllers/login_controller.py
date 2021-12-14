from flask import request
from http import HTTPStatus
from app.models.professionals_model import ProfessionalsModel
from app.models.patients_model import PatientModel
from flask_jwt_extended import create_access_token

def login():
   
    user_data = request.get_json()

    user_professional: ProfessionalsModel = ProfessionalsModel.query.filter_by(email=user_data["email"]).first()

    user_patient: PatientModel = PatientModel.query.filter_by(email=user_data["email"]).first()

    if user_professional:
        if user_professional.verify_password(user_data["password"]):
            access_token = create_access_token(identity=user_professional)
            
            return {"message": access_token}, HTTPStatus.OK
        else:
            return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED


    if user_patient: 
        if user_patient.verify_password(user_data["password"]):
            access_token = create_access_token(identity=user_patient)
            
     
            return {"message": access_token}, HTTPStatus.OK
        else:
            return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

    if not user_professional and not user_patient:
        return {"message": "User not found"}, HTTPStatus.NOT_FOUND
    
    
  
