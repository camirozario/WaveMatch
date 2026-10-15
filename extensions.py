from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Criação de objeto mas sem conexão ainda -> permite com que seja importado em outros arquivos além de app.py

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()