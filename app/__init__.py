from flask import Flask
from app.configs import env_configs, database, migration, jwt
from app.routes import api_blueprint
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    env_configs.init_app(app)
    database.init_app(app)
    migration.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(api_blueprint.bp)

    return app
