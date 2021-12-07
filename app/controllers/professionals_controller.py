from flask import jsonify, request, current_app
from app.models.professionals_model import ProfessionalsModel
# from app.configs.database import db

#criar profissional
def create_professional():
    data = request.json

    new_professional = ProfessionalsModel(**data)

    current_app.db.session.add(new_professional)

    current_app.db.session.commit()

    return jsonify(new_professional)

    # try:

    # except



#busca de todos od profissionais
def get_all_professionals():
    professionals = (ProfessionalsModel.query.all())
    result = [
        {
        "council_number": professional.council_number,
        "name": professional.name,
        "email": professional.email, 
        "phone": professional.phone,
        "password": professional.password ,
        "specialty": professional.specialty,
        "address": professional.address
        } for professional in professionals 
    ]

    return jsonify(result)

#busca por uma especialidade especifica
def filter_by_specialty(specialty):
    professionals = (ProfessionalsModel.query.filter_by(specialty=specialty))

    result = [
        {
        "council_number": professional.council_number,
        "name": professional.name,
        "email": professional.email, 
        "phone": professional.phone,
        "password": professional.password ,
        "specialty": professional.specialty,
        "address": professional.address
        } for professional in professionals 
    ]

    return jsonify(result)



#atualiza os dados do profissional
def update_professional(cod):
    data = request.json

    professional = ProfessionalsModel.query.filter_by(council_number=cod).update(data)

    current_app.db.session.commit()

    updated_profesional = ProfessionalsModel.query.get(cod)

    return jsonify(updated_profesional)

    


#deleta um profissional
def delete_professional(cod):
    
    professional = ProfessionalsModel.query.get_or_404(cod)

    current_app.db.session.delete(professional)
    current_app.db.session.commit()

    return jsonify(professional)


