from flask import jsonify, request, current_app
from sqlalchemy.sql.elements import and_
from app.controllers.professionals_controller import update_professional
from app.models.professionals_model import ProfessionalsModel
from app.models.patients_model import PatientModel
from app.models.appointments_model import AppointmentsModel
from datetime import date, datetime, time, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy import extract
import threading
import pywhatkit as wpp
# para emails
import os
import smtplib
from email.message import EmailMessage
# from app.configs.env_configs


def get_by_pacient(cpf):
    appointments = AppointmentsModel.query.filter(
        AppointmentsModel.patient_id == cpf)

    serializer = [
        {
            "date": appointment.date,
            "finished": appointment.finished,
            "pacient": appointment.patient.name,
            "doctor": appointment.professionals.name,
            "complaint": appointment.complaint
        } for appointment in appointments
    ]
    return jsonify(serializer), 200


def get_by_professional(council_number):
    appointments = AppointmentsModel.query.filter(
        AppointmentsModel.professionals_id == council_number)

    serializer = [
        {
            "date": appointment.date,
            "finished": appointment.finished,
            "pacient": appointment.patient.name,
            "doctor": appointment.professionals.name,
            "speciality": appointment.professionals.speciality,
            "complaint": appointment.complaint
        } for appointment in appointments
    ]
    return jsonify(serializer), 200


def get_by_date(date):
    date = date.split('-')
    date_appointment = AppointmentsModel.query.filter(
        extract('year', AppointmentsModel.date) == date[0], extract('month', AppointmentsModel.date) == date[1], extract('day', AppointmentsModel.date) == date[2])

    serializer = [
        {
            "date": appointment.date,
            "finished": appointment.finished,
            "pacient": appointment.patient.name,
            "doctor": appointment.professionals.name,
            "complaint": appointment.complaint
        } for appointment in date_appointment
    ]
    return jsonify(serializer), 200


def get_not_finished():
    not_finished_appointment = AppointmentsModel.query.filter(
        AppointmentsModel.finished == False)

    serializer = [
        {
            "date": appointment.date,
            "finished": appointment.finished,
            "pacient": appointment.patient.name,
            "doctor": appointment.professionals.name,
            "complaint": appointment.complaint
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
        return {"error": "Patient not found"}, 404

    temp_list_professionals = []
    for professional in all_professionals:
        temp_list_professionals.append(professional.council_number)

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

        # tentando enviar email:
        kwargs_email = {'date': date1, 'appointment': new_appointment}
        send_email_msg(**kwargs_email)
        return jsonify(new_appointment), 200
    except IntegrityError:
        return {"error": "There is already an appointment scheduled for this time"}, 409


def update_appointment(id):
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

    AppointmentsModel.query.filter_by(id=id).update(data)
    current_app.db.session.commit()

    updated_appointment = AppointmentsModel.query.get(id)

    if updated_appointment:
        return jsonify(updated_appointment), 200
    return {"error": "Appointment not found"}, 404


def get_24h():
    tomorrow = datetime.now().date()+timedelta(days=1)
    end_tomorrow = tomorrow+timedelta(days=1)
    appointments = AppointmentsModel.query.filter(
        and_(AppointmentsModel.date > tomorrow, AppointmentsModel.date < end_tomorrow))

    serializer = [
        {
            "doctor": appointment.professionals.name,
            "patient": appointment.patient.name,
            "date": appointment.date,
            "patient_phone": appointment.patient.phone,
            "patient_email": appointment.patient.email
        } for appointment in appointments
    ]

    return jsonify(serializer), 200


def send_wpp_msg(**kwargs):
    date = kwargs.get('date')
    appointment = kwargs.get('appointment')
    appointment_day = datetime.date(date)
    appointment_time = datetime.time(date)
    msg = f'Bom dia, {appointment.patient.name}! Voce marcou uma consulta em nossa clinica com {appointment.professionals.name} no dia {appointment_day} as {appointment_time}'
    phone = '+55'+appointment.patient.phone
    time_to_send = datetime.now() + timedelta(minutes=2)
    wpp.sendwhatmsg(phone, msg, time_to_send.hour,
                    time_to_send.minute, time_to_send.second)


def msg_all():
    now = datetime.now()
    appointments = AppointmentsModel.query.filter(and_(AppointmentsModel.date > (
        now+timedelta(days=1)), AppointmentsModel.date < (now+timedelta(days=2)))).all()

    for appointment in appointments:
        appointment_time = datetime.time(appointment.date)
        msg = f'Bom dia, {appointment.patient.name}! Vim te lembrar de sua consulta amanhã as {appointment_time} com {appointment.professionals.name}'
        time_to_send = datetime.now() + timedelta(minutes=2)
        phone = '+55'+appointment.patient.phone
        wpp.sendwhatmsg(phone, msg, time_to_send.hour,
                        time_to_send.minute, time_to_send.second)


# função para mandar email pro paciente
def send_email_msg(**kwargs):    
    date = kwargs.get('date')
    appointment = kwargs.get('appointment')
    appointment_day = datetime.date(date)
    appointment_time = datetime.time(date)

    # configurar email senha
    EMAIL_ADDRESS = 'kenziedocsecretary@gmail.com'
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

    # criar um email
    msg = EmailMessage()
    msg['Subject'] = f'Consulta com {appointment.professionals.speciality} na clínica KenzieDoc'
    msg['From'] = 'kenziedocsecretary@gmail.com'
    msg['To'] = f'{appointment.patient.email}'
    msg.set_content(f'''
        Prezado(a), {appointment.patient.name}

        Você tem uma consulta na clínica KenzieDoc com especialista em {appointment.professionals.speciality}, Dr(a) {appointment.professionals.name} 
        Consulta agendada para dia {appointment_day} às {appointment_time} horas

        Att,
        Secretária KenzieDoc
    '''        
        )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
