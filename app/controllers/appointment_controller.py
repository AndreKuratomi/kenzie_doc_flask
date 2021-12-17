from flask import app, jsonify, request, current_app
from sqlalchemy.sql.elements import and_
from app.controllers.professionals_controller import update_professional
from app.models.professionals_model import ProfessionalsModel
from app.models.patients_model import PatientModel
from app.models.appointments_model import AppointmentsModel
from datetime import date, datetime, time, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy import extract
from ipdb import set_trace
from flask_jwt_extended import jwt_required, get_jwt_identity
import math
from http import HTTPStatus

import threading
import pywhatkit as wpp

import os
import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")


@jwt_required()
def get_by_pacient(cpf):
    current_user = get_jwt_identity()

    if current_user['email'] == EMAIL_ADDRESS:
        appointments = AppointmentsModel.query.filter(
            AppointmentsModel.patient_id == cpf)

        serializer = [
            {   "id": appointment.id,
                "date": appointment.date,
                "finished": appointment.finished,
                "pacient": appointment.patient.name,
                "doctor": appointment.professional.name,
                "complaint": appointment.complaint
            } for appointment in appointments
        ]
        return jsonify(serializer), 200
    else:
        return jsonify({"message": "Unauthorized"}), HTTPStatus.UNAUTHORIZED

@jwt_required()
def get_by_professional(council_number):
    current_user = get_jwt_identity()

    if current_user['email'] == EMAIL_ADDRESS:
        appointments = AppointmentsModel.query.filter(
            AppointmentsModel.professionals_id == council_number.upper())

        serializer = [
            {
                "id": appointment.id,
                "date": appointment.date,
                "finished": appointment.finished,
                "pacient": appointment.patient.name,
                "doctor": appointment.professional.name,
                "speciality": appointment.professional.speciality,
                "complaint": appointment.complaint
            } for appointment in appointments
        ]
        return jsonify(serializer), 200
    else:
        return jsonify({"message": "Unauthorized"}), HTTPStatus.UNAUTHORIZED


@jwt_required()
def get_by_date(date):
    current_user = get_jwt_identity()

    if current_user['email'] == EMAIL_ADDRESS:

        date = date.split('-')
        date_appointment = AppointmentsModel.query.filter(
            extract('year', AppointmentsModel.date) == date[0], extract('month', AppointmentsModel.date) == date[1], extract('day', AppointmentsModel.date) == date[2])

        serializer = [
            {
                "id": appointment.id,
                "date": appointment.date,
                "finished": appointment.finished,
                "pacient": appointment.patient.name,
                "doctor": appointment.professional.name,
                "complaint": appointment.complaint
            } for appointment in date_appointment
        ]
        return jsonify(serializer), 200
    else:
        return jsonify({"message": "Unauthorized"}), HTTPStatus.UNAUTHORIZED


@jwt_required()
def get_not_finished():
    current_user = get_jwt_identity()

    if current_user['email'] == EMAIL_ADDRESS:

        not_finished_appointment = AppointmentsModel.query.filter(
            AppointmentsModel.finished == False)

        serializer = [
            {
                "id": appointment.id,
                "date": appointment.date,
                "finished": appointment.finished,
                "pacient": appointment.patient.name,
                "doctor": appointment.professional.name,
                "complaint": appointment.complaint
            } for appointment in not_finished_appointment
        ]

        return jsonify(serializer), 200
    else:
        return jsonify({"message": "Unauthorized"}), HTTPStatus.UNAUTHORIZED
        

@jwt_required()
def create_appointment():
    current_user = get_jwt_identity()

    if current_user['email'] == EMAIL_ADDRESS:
        required_keys = ['date', 'patient_id', 'professionals_id']
        data = request.json
        all_patients = PatientModel.query.all()
        all_professionals = ProfessionalsModel.query.all()

        temp_list_patients = []
        for patient in all_patients:
            temp_list_patients.append(patient.cpf)

        if data['patient_id'] not in temp_list_patients:
            return {"error": "Patient not found"}, 404

        temp_list_professionals = []
        for professional in all_professionals:
            temp_list_professionals.append(professional.council_number)

        if data['professionals_id']:
            data['professionals_id'] = data['professionals_id'].upper()

        if data['professionals_id'] not in temp_list_professionals:
            return {"error": "Professional not found"}, 404

        for key in required_keys:
            if key not in data:
                return {"error": f"Key '{key}' missing"}, 400

        for key in data:
            if type(data[key]) != str:
                return {"error": "Fields must be strings"}, 400
            if key not in [*required_keys, 'complaint']:
                return {"error": f"Key '{key}' is invalid"}, 400

        date1 = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%SZ')
        date2 = datetime.now()
        if date2 > date1:
            return {"error": "You can`t schedule an appointment in the past!"}, 400

        try:
            new_appointment = AppointmentsModel(**data)
            current_app.db.session.add(new_appointment)
            current_app.db.session.commit()
            name = new_appointment.patient.name

            thread = threading.Thread(
                target=send_wpp_msg, kwargs={'date': date1, 'appointment': new_appointment})
            thread.start()

            kwargs_email = {'date': date1, 'appointment': new_appointment}
            send_email_msg(**kwargs_email)
            return jsonify(new_appointment), 200
        except IntegrityError:
            return {"error": "There is already an appointment scheduled for this time"}, 409
    else:
        return jsonify({"message": "Unauthorized"}), HTTPStatus.UNAUTHORIZED


@jwt_required()
def update_appointment(id):
    current_user = get_jwt_identity()

    accepted_keys = ['date', 'finished']
    data = request.json

    for key in data:
        if key not in accepted_keys:
            return {"error": f"Key '{key}' can`t be updated"}, 400

    if 'date' in data:
        if type(data['date']) != str:
            return {"msg": "Date must be a string"}, 400
        date1 = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%SZ')
        date2 = datetime.now()
        if date2 > date1:
            return {"error": "You can`t schedule an appointment in the past!"}, 400

    if 'finished' in data:
        if type(data['finished']) != bool:
            return {"error": "Finished must be a boolean"}, 400

    if current_user['email'] == EMAIL_ADDRESS:
        try:
            AppointmentsModel.query.filter_by(id=id).update(data)
            current_app.db.session.commit()
        except IntegrityError:
            return {"error": "There is already an appointment scheduled for this time"}, 409

        updated_appointment = AppointmentsModel.query.get(id)

        if updated_appointment:
            if 'date' in data:
                thread = threading.Thread(
                    target=send_update_wpp, kwargs={'appointment': updated_appointment, 'patient': updated_appointment.patient, 'doctor': updated_appointment.professional})
                thread.start()
                return jsonify(updated_appointment), 200
        return {"error": "Appointment not found"}, 404

    return jsonify({"message": "Unauthorized"}), HTTPStatus.UNAUTHORIZED


@jwt_required()
def get_24h():
    current_user = get_jwt_identity()

    if current_user['email'] == EMAIL_ADDRESS:

        tomorrow = datetime.now().date()+timedelta(days=1)
        end_tomorrow = tomorrow+timedelta(days=1)
        appointments = AppointmentsModel.query.filter(
            and_(AppointmentsModel.date > tomorrow, AppointmentsModel.date < end_tomorrow))

        serializer = [
            {
                "id": appointment.id,
                "doctor": appointment.professional.name,
                "patient": appointment.patient.name,
                "date": appointment.date,
                "patient_phone": appointment.patient.phone,
                "patient_email": appointment.patient.email
            } for appointment in appointments
        ]

        return jsonify(serializer), 200
    else:
        return jsonify({"message": "Unauthorized"}), HTTPStatus.UNAUTHORIZED

@jwt_required()
def get_wait_list(council_number):
    current_user = get_jwt_identity()

    if current_user['email'] == EMAIL_ADDRESS:
        doctor = ProfessionalsModel.query.get(council_number.upper())
        appointments = AppointmentsModel.query.filter(
            AppointmentsModel.professionals_id == council_number.upper()).all()

        not_finished = []

        for appointment in appointments:
            if appointment.date < datetime.now() and not appointment.finished:
                not_finished.append(appointment)

        average_time = len(not_finished) * 30
        hours = math.floor(average_time / 60)
        minutes = average_time % 60

        return {'msg': f'Existem {len(not_finished)} pessoas esperando para serem atendidas pelo(a) Dr(a). {doctor.name}. Tempo médio de espera é de {hours} horas e {minutes} minutos'}

    else:
        return jsonify({"message": "Unauthorized"}), HTTPStatus.UNAUTHORIZED

@jwt_required()
def delete_appointment(id):
    current_user = get_jwt_identity()

    try:
        appointment = AppointmentsModel.query.get(id)

        if current_user['email'] == EMAIL_ADDRESS:
            current_app.db.session.delete(appointment)
            current_app.db.session.commit()
            return {}, 204

        return jsonify({"message": "Unauthorized"}), HTTPStatus.UNAUTHORIZED

    except UnmappedInstanceError:
        return {"error": "appointment not found"}, 404


def send_wpp_msg(**kwargs):
    date = kwargs.get('date')
    appointment = kwargs.get('appointment')
    weekday = get_weekday(date.weekday())
    msg = f'Bom dia, {appointment.patient.name}! Você marcou uma consulta em nossa clinica com {appointment.professional.name} na {weekday}, dia {datetime.strftime(date, "%d/%m/%Y")} às {datetime.strftime(date, "%H:%M")}'
    phone = '+55'+appointment.patient.phone
    time_to_send = datetime.now() + timedelta(minutes=1)
    wpp.sendwhatmsg(phone, msg, time_to_send.hour,
                    time_to_send.minute)

def msg_all():
    now = datetime.now()
    appointments = AppointmentsModel.query.filter(and_(AppointmentsModel.date > (
        now+timedelta(days=1)), AppointmentsModel.date < (now+timedelta(days=2)))).all()

    for appointment in appointments:
        appointment_time = datetime.time(appointment.date)
        msg = f'Bom dia, {appointment.patient.name}! Vim te lembrar de sua consulta amanhã as {appointment_time} com {appointment.professional.name}'
        time_to_send = datetime.now() + timedelta(minutes=2)
        phone = '+55'+appointment.patient.phone
        wpp.sendwhatmsg(phone, msg, time_to_send.hour,
                        time_to_send.minute, time_to_send.second)


def send_email_msg(**kwargs):
    date = kwargs.get('date')
    appointment = kwargs.get('appointment')
    appointment_day = datetime.strftime(date, "%d/%m/%Y")
    appointment_time = datetime.strftime(date, "%H:%M")

    msg = EmailMessage()
    msg['Subject'] = f'Consulta com {appointment.professional.speciality} na clínica KenzieDoc'
    msg['From'] = EMAIL_PASSWORD
    msg['To'] = f'{appointment.patient.email}'
    msg.set_content(f'''
        Prezado(a), {appointment.patient.name}

        Você tem uma consulta na clínica KenzieDoc com especialista em {appointment.professional.speciality}, Dr(a) {appointment.professional.name} 
        Consulta agendada para dia {appointment_day} às {appointment_time} horas

        Att,
        Secretária KenzieDoc
    '''
                    )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


def send_update_wpp(**kwargs):
    appointment = kwargs['appointment']
    patient = kwargs['patient']
    doctor = kwargs['doctor']
    date = appointment.date
    msg = f'Olá, {patient.name}, sua consulta com {doctor.name} foi remarcada para {datetime.strftime(date, "%d/%m/%Y")} às {datetime.strftime(date, "%H:%M")}'
    phone = '+55'+patient.phone
    time_to_send = datetime.now() + timedelta(minutes=1)
    wpp.sendwhatmsg(phone, msg, time_to_send.hour,
                    time_to_send.minute)


def get_weekday(n):
    return {
        0: 'segunda-feira',
        1: 'terça-feira',
        2: 'quarta-feira',
        3: 'quinta-feira',
        4: 'sexta-feira',
        5: 'sábado',
        6: 'domingo',
    }[n]
