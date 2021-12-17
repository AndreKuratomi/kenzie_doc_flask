from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={"expire_on_commit": False})


def init_app(app: Flask):
    db.init_app(app)
    app.db = db
