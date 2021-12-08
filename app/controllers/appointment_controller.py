from flask import jsonify
from app.models.appointments_model import AppointmentsModel


#busca de todas as consultas
def get_by_pacient(cpf):
    #nao serie pelo id ?
    pacient = AppointmentsModel.query.filter(AppointmentsModel.patient.cpf == cpf)
    return jsonify(pacient), 200


#busca por um profissional
def get_by_professional(cod):
    professional = AppointmentsModel.query.filter(AppointmentsModel.professionals_id == cod)
    return jsonify(professional), 200
    

#busca por data especifica
def get_by_date(date):
    date_appointment = AppointmentsModel.query.filter(AppointmentsModel.date == date)
    return jsonify(date_appointment), 200
    

#buscar consultas não concluidas
def get_not_finished():
    not_finished_appointment = AppointmentsModel.query.filter(AppointmentsModel.finished == False)
    return jsonify(not_finished_appointment), 200



 