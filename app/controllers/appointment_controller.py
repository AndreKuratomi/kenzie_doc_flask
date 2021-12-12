from flask import jsonify, request, current_app
from app.controllers.professionals_controller import update_professional
from app.models.professionals_model import ProfessionalsModel
from app.models.patients_model import PatientModel
from app.models.appointments_model import AppointmentsModel
from datetime import date, datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import extract
from ipdb import set_trace
# busca de todas as consultas


def get_by_pacient(cpf):
    appointments = AppointmentsModel.query.filter(
        AppointmentsModel.patient_id == cpf)

    serializer = [
        {
            "date": appointment.date,
            "finished": appointment.finished,
            "pacient": appointment.patient.name,
            "doctor": appointment.professionals.name
        } for appointment in appointments
    ]
    return jsonify(serializer), 200


# busca por um profissional
def get_by_professional(council_number):
    professionals_appointments = AppointmentsModel.query.filter(
        AppointmentsModel.professionals_id == council_number)

    serializer = [
        {
            "date": professional.date,
            "finished": professional.finished,
            "pacient": professional.patient.name,
            "doctor": professional.professionals.name,
            "speciality": professional.professionals.speciality
        } for professional in professionals_appointments
    ]
    return jsonify(serializer), 200


# busca por data especifica
def get_by_date(date):
    date = date.split('-')
    date_appointment = AppointmentsModel.query.filter(
        extract('year', AppointmentsModel.date) == date[0], extract('month', AppointmentsModel.date) == date[1], extract('day', AppointmentsModel.date) == date[2])

    serializer = [
        {
            "date": appointment.date,
            "finished": appointment.finished,
            "pacient": appointment.patient.name,
            "doctor": appointment.professionals.name
        } for appointment in date_appointment
    ]
    return jsonify(serializer), 200


# buscar consultas não concluidas
def get_not_finished():
    not_finished_appointment = AppointmentsModel.query.filter(
        AppointmentsModel.finished == False)

    serializer = [
        {
            "date": appointment.date,
            "finished": appointment.finished,
            "pacient": appointment.patient.name,
            "doctor": appointment.professionals.name
        } for appointment in not_finished_appointment
    ]
    return jsonify(serializer), 200


def create_appointment():
    required_keys = ['date', 'patient_id', 'professionals_id']

    data = request.json
    
    all_patients = PatientModel.query.all()
    all_professionals = ProfessionalsModel.query.all()

    temp_list_patients = []
    for patient in all_patients:
        temp_list_patients.append(patient.cpf)

    if data['patient_id'] not in temp_list_patients:
        return {"msg": "Patient not found"}, 404

    temp_list_professionals = []
    for professional in all_professionals:
        temp_list_professionals.append(professional.council_number)

    if data['professionals_id'] not in temp_list_professionals:
        return {"msg": "Professional not found"}, 404

    for key in required_keys:
        if key not in data:
            return {"msg": f"Key '{key}' missing"}, 400

    for key in data:
        print(key)
        if type(data[key]) != str:
            return {"msg": "Fields must be strings"}, 400
        if key not in required_keys:
            return {"msg": f"Key '{key}' is invalid"}, 400

    date1 = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%SZ')
    date2 = datetime.now()
    if date2 > date1:
        return {"msg": "You can`t schedule an appointment in the past!"}, 400

    try:
        new_appointment = AppointmentsModel(**data)
        current_app.db.session.add(new_appointment)
        current_app.db.session.commit()
        return jsonify(new_appointment), 200

<<<<<<< HEAD
=======
    # except NotFound 

>>>>>>> 28e745c0c208810d1cede4d57218c0fb8acabee5
    except IntegrityError:
        return {"msg": "There is already an appointment scheduled for this time"}, 409


def update_appointment(id):
    accepted_keys = ['date', 'finished']
    data = request.json

    for key in data:
        if key not in accepted_keys:
            return {"msg": f"Key '{key}' can`t be updated"}, 400

    if 'date' in data:
        if type(data['date']) != str:
            return {"msg": "Date must be a string"}, 400
        date1 = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%SZ')
        date2 = datetime.now()
        if date2 > date1:
            return {"msg": "You can`t schedule an appointment in the past!"}, 400

    if 'finished' in data:
        if type(data['finished']) != bool:
            return {"msg": "Finished must be a boolean"}, 400

    AppointmentsModel.query.filter_by(id=id).update(data)
    current_app.db.session.commit()

    updated_appointment = AppointmentsModel.query.get(id)

    if updated_appointment:
        return jsonify(updated_appointment), 200
    return {"msg": "Appointment not found"}, 404
