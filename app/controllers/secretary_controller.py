from flask import jsonify, request, current_app

from app.models.secretary_model import SecretaryModel
from sqlalchemy.exc import IntegrityError
import re


def create_secretary():
    try:
        required_keys = ['name', 'email', 'phone']

        data = request.json

        password_to_hash = data.pop("password")
        for key in data:
            if key != 'password' and key not in required_keys:
                raise KeyError
            if type(data[key]) != str:
                return {"error": "Fields must be strings"}, 422

        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data['email']):
            return {"error": "Invalid email. Correct example yourname@provider.com"}, 400

        if not re.fullmatch(r"^(\([0-9]{2}\)[0-9]{5}-)[0-9]{4}$", data['phone']):
            return jsonify({"error": "Invalid phone number format. Correct example (xx)xxxxx-xxxx"}), 400

        data['password'] = password_to_hash
        if type(data['password']) != str:
            return {"error": "Invalid field 'password'. It must be an string"}, 400

        secretary = SecretaryModel(**data)

        current_app.db.session.add(secretary)
        current_app.db.session.commit()
        return jsonify(secretary), 201
    except IntegrityError as e:
        return {"error": "secretary already exists"}, 409

    except KeyError as e:
        return {"error": f"The key {e} is not valid"}, 400
