from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text # Tansforma SQL textual em algo que ele possa executar no SQLAlchemy. Para isso, usamos a função text().
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token
import os
from dotenv import load_dotenv


#Definindo a aplicação Flask
app = Flask(__name__) # O __name__ é uma variável especial do Python. Quando você executa o python app.py o python define __name__ == "__main__"
load_dotenv()
# Configurações do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") #Ela diz ao SQLAlchemy onde está o banco e como chegar nele.
# postgresql →  banco que quero usar é PostgreSQL.
# psycopg → Use o Psycopg para Python conversar com PostgreSQL
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
print("JWT no Flask:", app.config["JWT_SECRET_KEY"] is not None)


db = SQLAlchemy(app) # Crie uma instância/objeto de SQLAlchemy, configurada para trabalhar com a minha aplicação Flask app, e guarde esse objeto na variável db
jwt = JWTManager(app)



class User(db.Model): # User será um modelo de dados gerenciado pelo meu objeto db
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False, unique=True)
    password_hash = db.Column(db.String(255),nullable=False)
    surf_level = db.Column(db.String(50),nullable=False)
    min_wave_height = db.Column(db.Float,nullable=True)
    max_wave_height = db.Column(db.Float, nullable=True)


#Rotas
@app.route('/')
def home():
    result = db.session.execute(text("SELECT 1"))  #Executa a query SQL e retorna o resultado(número 1).
    return "Database connected"

@app.route('/register', methods=['POST'])
def create_user():
    data = request.get_json() # Pega os dados enviados pelo cliente e transforma em um dicionário Python
    name = data.get('name')
    email = data.get('email')
    password_hash = generate_password_hash(data.get('password'))
    surf_level = data.get('surf_level')
    min_wave_height = data.get('min_wave_height')
    max_wave_height = data.get('max_wave_height')

    new_user = User(
        name = name,
        email = email,
        password_hash = password_hash,
        surf_level = surf_level,
        min_wave_height = min_wave_height,
        max_wave_height = max_wave_height
    )

    db.session.add(new_user) # Adiciona o novo usuário à sessão do banco de dados
    db.session.commit() # Salva as alterações no banco de dados

    return jsonify({"message": "Sua conta foi criada com sucesso!", "id": new_user.id}), 201 # HTTP status code > 201 significa Created

@app.route( '/users/<int:user_id>', methods = ['GET'])
def get_user(user_id):
    user = db.session.get(User,user_id) # Na sessão do banco (db.session), pegue (get) um objeto do modelo User cuja primary key seja user_id
    # retorna none se não encontrar

    if user is None:
        return jsonify ({"message": 'Usuário não encontrado'}),404
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email
        })

@app.route('/users/<int:user_id>', methods = ['PUT'])
def update_user(user_id):
    user = db.session.get(User,user_id)

    if user is None:
        return jsonify ({'message': 'usuário não encontrado'}),404

    data = request.get_json()
    if 'surf_level' in data:
        user.surf_level = data.get('surf_level')

    if 'min_wave_height' in data:
        user.min_wave_height = data.get('min_wave_height')

    if 'max_wave_height' in data:
        user.max_wave_height = data.get('max_wave_height')

    db.session.commit()

    return jsonify({'message':'Informações atualizadas com sucesso!'}),200

@app.route('/users/<int:user_id>', methods = ['DELETE'])
def delete_account(user_id):
    user = db.session.get(User,user_id)

    if user is None:
        return jsonify({'message':'Usuário não encontrado'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message':'user deleted successfuly'}),200


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = db.session.execute(
        db.select(User).where(User.email == email)
    ).scalar_one_or_none()

    if user is None:
        return jsonify({'message':'Email ou senha inválidos'}),401

    if not check_password_hash(user.password_hash, password):
        return jsonify({'message':'Email ou senha inválidos'}),401

    access_token = create_access_token(identity=str(user.id)) # identidade do JWT (sub, de subject) é esperada como string nesse contexto
    return jsonify({'message':'login validado com sucesso',
                    'access_token':access_token}),200


if __name__ == '__main__':
    app.run(debug=True) 