import os
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text # Tansforma SQL textual em algo que ele possa executar no SQLAlchemy. Para isso, usamos a função text().
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from flask_migrate import Migrate
from dotenv import load_dotenv
from datetime import datetime
from statistics import mean
from flask_cors import CORS
from flasgger import Swagger



#Definindo a aplicação Flask
app = Flask(__name__) # O __name__ é uma variável especial do Python. Quando você executa o python app.py o python define __name__ == "__main__"
CORS(app)
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "WaveMatch API",
        "version": "1.0.0",
        "description": "API de recomendações de surf."
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Insira: Bearer <seu_token_JWT>"
        }
    }
}
swagger = Swagger(app, template=swagger_template)

load_dotenv()


# Configurações do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") #Ela diz ao SQLAlchemy onde está o banco e como chegar nele.
# postgresql →  banco que quero usar é PostgreSQL.
# psycopg → Use o Psycopg para Python conversar com PostgreSQL
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")


db = SQLAlchemy(app) # Crie uma instância/objeto de SQLAlchemy, configurada para trabalhar com a minha aplicação Flask app, e guarde esse objeto na variável db
jwt = JWTManager(app)
migrate = Migrate(app,db)

class User(db.Model): # User será um modelo de dados gerenciado pelo meu objeto db
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False, unique=True)
    password_hash = db.Column(db.String(255),nullable=False)
    surf_level = db.Column(db.String(50),nullable=False)
    min_wave_height = db.Column(db.Float,nullable=True)
    max_wave_height = db.Column(db.Float, nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)

class SurfSpot(db.Model):
    __tablename__= 'surf_spot'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100),nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    beach_orientation = db.Column(db.Float, nullable=True)
    surf_level = db.Column(db.String(50), nullable=False)
    wave_direction = db.Column(db.String(100))
    predominant_direction = db.Column(db.String(100))
    wave_shape = db.Column(db.String(100))
    wave_duration = db.Column(db.String(100))
    wave_speed = db.Column(db.String(100))
    break_length = db.Column(db.String(100))
    current_tendency = db.Column(db.String(100))
    
    

#=================
#FUNÇÕES AUXILIARES
#=================

def get_marine_data(spot):
    params_marine = {
            'latitude': spot.latitude,
            'longitude': spot.longitude,
            'hourly': 'wave_height,wave_period,swell_wave_direction,swell_wave_period',
            'timezone': 'America/Sao_Paulo'
        }
    #params é simplesmente um dicionário Python que nós criamos para dizer à API externa quais informações estamos enviando/pedindo.


    #url api externa
    url_marine = 'https://marine-api.open-meteo.com/v1/marine'
    response_marine = requests.get(url_marine, # para onde eu quero mandar o GET
                            params=params_marine) # quais parâmetros quero mandar
    #response ainda não é o JSON. É um objeto que representa a resposta HTTP inteira
    data_marine = response_marine.json()

    return data_marine

def get_wind_data(spot):
    params_wind = {    
        'latitude': spot.latitude,
        'longitude': spot.longitude,
        'hourly':'wind_speed_10m,wind_direction_10m',
        'timezone': 'America/Sao_Paulo'
    }

    url_wind = 'https://api.open-meteo.com/v1/forecast'
    response_wind = requests.get(url_wind,params=params_wind)
    data_wind = response_wind.json()

    return data_wind

def get_ubatuba_weather():

    params_weather = {
        'latitude': -23.4339,
        'longitude': -45.0833,
        'current': 'temperature_2m,weather_code',
        'timezone': 'America/Sao_Paulo'
    }

    url_weather = 'https://api.open-meteo.com/v1/forecast'

    response_weather = requests.get(
        url_weather,
        params=params_weather
    )

    return response_weather.json()

def evaluate_weather(weather_code, temperature):

    # Ensolarado
    if weather_code in [0, 1]:

        if temperature < 20:
            return {
                'condition': 'ensolarado_frio',
                'condition_text': 'ensolarado',
                'message': 'Sol lá fora, mas eu levaria um john para o surf!'
            }

        else:
            return {
                'condition': 'ensolarado',
                'condition_text': 'ensolarado',
                'message': 'Sol perfeito para aproveitar o mar!'
            }

    # Nublado
    elif weather_code in [2, 3, 45, 48]:
        return {
            'condition': 'nublado',
            'condition_text': 'nublado',
            'message': 'Bora animar o dia surfando?'
        }

    # Garoa ou chuva
    elif weather_code in [
        51, 53, 55, 56, 57,
        61, 63, 65, 66, 67,
        80, 81, 82
    ]:
        return {
            'condition': 'chuvoso',
            'condition_text': 'chuvoso',
            'message': 'Vai precisar de coragem para surfar hoje!'
        }

    # Neve
    elif weather_code in [71, 73, 75, 77, 85, 86]:
        return {
            'condition': 'frio',
            'condition_text': 'frio',
            'message': 'Hoje eu definitivamente levaria um john para o surf!'
        }

    # Tempestade
    elif weather_code in [95, 96, 99]:
        return {
            'condition': 'tempestade',
            'condition_text': 'com tempestade',
            'message': 'Hoje vale acompanhar as condições antes de entrar no mar.'
        }

    else:
        return {
            'condition': 'indefinido',
            'condition_text': 'com condições variáveis',
            'message': 'Bora conferir como estão as condições para o surf hoje?'
        }
    
    
#score altura da onda
def evaluate_wave_height(wave_height, min_wave_height, max_wave_height):

    ideal_wave_height = (min_wave_height + max_wave_height) / 2

    if wave_height == ideal_wave_height: 
        return 100

    elif wave_height ==min_wave_height:
        return 50

    elif wave_height == max_wave_height:
        return 50

    elif min_wave_height < wave_height < ideal_wave_height:
        return round(100 - abs(wave_height - ideal_wave_height) / abs(ideal_wave_height - min_wave_height) * 50,2)

    elif ideal_wave_height < wave_height < max_wave_height:
        return round(100 - abs(wave_height - ideal_wave_height) / abs(ideal_wave_height - max_wave_height) * 50,2)

    elif wave_height <min_wave_height:
        score = 50 - abs(min_wave_height - wave_height) / abs(ideal_wave_height - min_wave_height) * 50
        return round(max(0, score), 2)

    elif wave_height > max_wave_height:
        score = 50 - abs(max_wave_height - wave_height) / abs(ideal_wave_height - max_wave_height) * 50
        return round(max(0, score), 2)

#Score Velocidade do Vento
def evaluate_wind_speed(wind_speed):

    if wind_speed <= 5:
        return 100

    elif wind_speed <= 10:
        return 90

    elif wind_speed <= 15:
        return 75

    elif wind_speed <= 20:
        return 55

    elif wind_speed <= 25:
        return 35

    elif wind_speed <= 30:
        return 15

    else:
        return 0

def evaluate_wind_direction(wind_direction,beach_orientation):
    difference = abs(wind_direction - beach_orientation)

    if difference > 180:
        difference = 360-difference

      # 0° = totalmente onshore
    if difference <= 30:
        return 20

    # Entre onshore e lateral
    elif difference <= 60:
        return 45

    # Vento lateral (cross-shore)
    elif difference <= 120:
        return 70

    # Entre lateral e offshore
    elif difference <= 150:
        return 90

    # 180° = totalmente offshore
    else:
        return 100

def evaluate_surf_level(user_level, spot_level):

    level_factors = {
        'iniciante': {
            'iniciante': 1.0,
            'intermediario': 0.65,
            'avancado': 0.30
        },

        'intermediario': {
            'iniciante': 0.90,
            'intermediario': 1.0,
            'avancado': 0.70
        },

        'avancado': {
            'iniciante': 0.80,
            'intermediario': 0.95,
            'avancado': 1.0
        }
    }

    return level_factors[user_level][spot_level]
#=================
#ROTAS
#=================

#=================
#PROFILE
#=================
@app.route('/profile', methods = ['GET'])
@jwt_required()
def get_profile():
    """
    Consulta dados do Usuário
    ---
    tags:
      - Profile
    security:
      - Bearer: []  
    responses:
      200:
        description: Dados Obtidos com sucesso
        schema:
          type: object
          properties:
            id: 
              type: integer
            name:
              type: string
            email:
              type: string
            date_of_birth:
              type: string
              format: date
            surf_level:
              type: string
            min_wave_height:
              type: number
            max_wave_height:
              type: number  
      401:
        description: Token ausente, inválido ou expirado.

      404:
        description: Usuário não encontrado.
    """
    user_id = get_jwt_identity() #
    user = db.session.get(User,int(user_id))

    if user is None:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
        'surf_level': user.surf_level,
        'min_wave_height': user.min_wave_height,
        'max_wave_height': user.max_wave_height
    }), 200


@app.route('/profile', methods = ['PUT'])
@jwt_required()
def update_user():
    """
    Atualizar dados do usuário
    ---
    tags:
      - Profile

    security:
      - Bearer: []

    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            surf_level:
              type: string
              enum:
                - iniciante
                - intermediario
                - avancado

            max_wave_height:
              type: number
              example: 1.5

            min_wave_height:
              type: number
              example: 0.5

    responses:
      200:
        description: Informações atualizadas com sucesso.

      401:
        description: Token ausente, inválido ou expirado.

      404:
        description: Usuário não encontrado.
    """
    user_id = get_jwt_identity() #pega a identidade que foi armazenada dentro do JWT quando fizemos o login.

    user = db.session.get(User, int(user_id))

    if user is None:
        return jsonify ({'message': 'Usuário não encontrado'}),404

    data = request.get_json()
    if 'surf_level' in data:
        user.surf_level = data.get('surf_level')

    if 'min_wave_height' in data:
        user.min_wave_height = data.get('min_wave_height')

    if 'max_wave_height' in data:
        user.max_wave_height = data.get('max_wave_height')

    db.session.commit()

    return jsonify({'message':'Informações atualizadas com sucesso!'}),200

@app.route('/profile', methods = ['DELETE'])
@jwt_required()
def delete_account():
    """
    Excluir conta do usuário
    ---
    tags:
      - Profile

    security:
      - Bearer: []

    responses:
      200:
        description: Conta excluída com sucesso.

      401:
        description: Token ausente, inválido ou expirado.

      404:
        description: Usuário não encontrado.
    """
    user_id = get_jwt_identity()

    user = db.session.get(User,int(user_id))

    if user is None:
        return jsonify({'message':'Usuário não encontrado'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message':'user deleted successfuly'}),200


#=================
#USER
#=================

@app.route('/login', methods=['POST'])
def login():
    """
    Permite o login do usuario atraves da geracao de token JWT
    ---
    tags:
        - User

    parameters:
        - in: body
          name: body
          required: true
          schema:
            type: object
            required:
                - email
                - password
            properties:
                email:
                    type: string
                    example: camilla@email.com
                password:
                    type: string
                    example: minhaSenha123

    responses:
        200:
            description: Usuario autenticado com sucesso
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: login validado com sucesso
                    access_token:
                        type: string
                        example: token_jwt

        401:
            description: Email ou senha invalidos
    """

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

    access_token = create_access_token(identity=str(user.id)) # identidade do JWT (sub, de subject) é esperada como string nesse contexto / guarda id no jwt
    return jsonify({'message':'login validado com sucesso',
                    'access_token':access_token}), 200


@app.route('/register', methods=['POST'])
def create_user():
    """
    Cadastra um novo usuário no WaveMatch.
    ---
    tags:
      - User

    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - password
            - surf_level
          properties:
            name:
              type: string
              example: Marina

            email:
              type: string
              example: marina@email.com

            password:
              type: string
              format: password
              example: minhaSenha123

            surf_level:
              type: string
              enum:
                - iniciante
                - intermediario
                - avancado

            min_wave_height:
              type: number
              example: 0.5

            max_wave_height:
              type: number
              example: 1.5

            date_of_birth:
              type: string
              format: date
              example: "2000-05-15"

    responses:
      201:
        description: Usuário cadastrado com sucesso.

      409:
        description: E-mail já registrado.
    """
    data = request.get_json() # Pega os dados enviados pelo cliente e transforma em um dicionário Python
    email = data.get('email')
    verify_email=db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar_one_or_none()

    if verify_email is not None:
            return jsonify ({'message': 'Email já registrado'}), 409 # conflict

    name = data.get('name')
    surf_level = data.get('surf_level')
    min_wave_height = data.get('min_wave_height')
    max_wave_height = data.get('max_wave_height')
    password_hash = generate_password_hash(data.get('password'))

    new_user = User(
        name = name,
        email = email,
        password_hash = password_hash,
        surf_level = surf_level,
        min_wave_height = min_wave_height,
        max_wave_height = max_wave_height)

    db.session.add(new_user) # Adiciona o novo usuário à sessão do banco de dados
    db.session.commit() # Salva as alterações no banco de dados

    
    return jsonify({"message": "Sua conta foi criada com sucesso!", "id": new_user.id}), 201 # HTTP status code > 201 significa Created


#=================
#DASHBOARD
#=================

@app.route('/dashboard_info', methods=['GET'])
@jwt_required()
def dashboard_info():
    """
    Obtém dados básicos apresentados no dashboard principal.
    ---
    tags:
      - Dashboard

    security:
      - Bearer: []

    responses:
      200:
        description: Dados recebidos com sucesso.
        schema:
          type: object
          properties:
            name:
              type: string
            temperature:
              type: number
              format: float
            condition:
              type: string
            condition_text:
              type: string
            message:
              type: string

      401:
        description: Token ausente, inválido ou expirado.
    """

    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    weather_data = get_ubatuba_weather()

    temperature = weather_data['current']['temperature_2m']
    weather_code = weather_data['current']['weather_code']

    weather = evaluate_weather(weather_code, temperature)

    return jsonify({
        'name': user.name,
        'temperature': temperature,
        'condition': weather['condition'],
        'condition_text': weather['condition_text'],
        'message': weather['message']
    }), 200

@app.route('/user_main_dashboard',methods =['GET'])
@jwt_required()
def user_recommendations():
    """
    Retorna as três melhores praias e os períodos
    recomendados conforme o perfil do usuário.
    ---
    tags:
      - Dashboard

    security:
      - Bearer: []

    responses:
      200:
        description: Recomendações obtidas com sucesso.
        schema:
          type: object
          additionalProperties:
            type: object
            properties:
              best_score:
                type: number
                format: float

              periodos:
                type: array
                items:
                  type: object
                  properties:
                    periodo:
                      type: string
                      example: manhã

                    score:
                      type: number
                      format: float

      401:
        description: Token ausente, inválido ou expirado.
    """
    #get user
    current_user_id = get_jwt_identity()
    user = db.session.get(User,int(current_user_id))

    spots = db.session.execute(
        db.select(SurfSpot)
    ).scalars().all() #Busca Todos meus SurfSpots
    best_spots = []
    today = datetime.now().date()

    if user.min_wave_height is not None:
        min_wave_height = user.min_wave_height

    elif user.surf_level == 'iniciante':
        min_wave_height = 0.4

    elif user.surf_level == 'intermediario':
        min_wave_height = 0.8

    elif user.surf_level == 'avancado':
        min_wave_height = 1

    if user.max_wave_height is not None:
        max_wave_height = user.max_wave_height

    elif user.surf_level == 'iniciante':
        max_wave_height = 1.5

    elif user.surf_level == 'intermediário':
        max_wave_height = 2

    elif user.surf_level == 'avançado':
        max_wave_height = 3



    for spot in spots:
        wave_heights_scores = {}
        wind_speeds_scores = {}
        wind_directions_scores ={}

        # Calcula compatibilidade entre nivel do usuario e nivel da praia
        level_factor = evaluate_surf_level(
            user.surf_level,
            spot.surf_level
        )
        # Busca dados externos
        data_marine = get_marine_data(spot)
        data_wind = get_wind_data(spot)

        wave_times = data_marine['hourly']['time']
        wave_heights = data_marine['hourly']['wave_height']

        wind_times = data_wind['hourly']['time']
        wind_speeds = data_wind['hourly']['wind_speed_10m']
        wind_directions = data_wind['hourly']['wind_direction_10m']

        # Organiza dados de vento por horario
        wind_forecast = {}

        for wind_time, wind_speed, wind_direction in zip(
                                                        wind_times,
                                                        wind_speeds,
                                                        wind_directions
                                                         ):
            wind_forecast[wind_time] = {
                'wind_speed': wind_speed,
                'wind_direction': wind_direction
                }

        for wave_time,wave_height in zip(wave_times,wave_heights):
            if wave_time in wind_forecast:
                wind_data = wind_forecast[wave_time]
                wind_speed = wind_data['wind_speed']
                wind_direction = wind_data['wind_direction']

            if datetime.fromisoformat(wave_time).date() == today:
                hour = datetime.fromisoformat(wave_time).hour
                periodo = None

                if 5 <= hour < 7:
                    periodo = 'amanhecer'

                elif 7 <= hour < 12:
                    periodo = 'manhã'

                elif 12 <= hour < 16:
                    periodo = 'tarde'

                elif 16 <= hour < 19:
                    periodo = 'fim da tarde'

                if periodo is not None:
                    wave_height_score = evaluate_wave_height(wave_height,
                                                             min_wave_height,
                                                             max_wave_height)
                    wind_speed_score = evaluate_wind_speed(wind_speed)
                    wind_direction_score = evaluate_wind_direction(wind_direction,spot.beach_orientation)



                    if periodo not in wave_heights_scores:
                        wave_heights_scores[periodo] =[]
                        wind_speeds_scores[periodo] =[]
                        wind_directions_scores[periodo] =[]

                    wave_heights_scores[periodo].append(wave_height_score)
                    wind_speeds_scores[periodo].append(wind_speed_score)
                    wind_directions_scores[periodo].append(wind_direction_score)

        # Calcula media de cada periodo
        for periodo, scores in  wave_heights_scores.items(): #chave e valor juntos
            wave_height_mean = mean(scores)
            wind_speed_mean = mean(wind_speeds_scores[periodo])
            wind_direction_mean=mean(wind_directions_scores[periodo])

            # Score das condicoes
            condition_score = (wave_height_mean * 0.6 + wind_speed_mean * 0.15 + wind_direction_mean*0.25)
            score = condition_score * level_factor

            

            best_spots.append({'name':spot.name,
                            'periodo':periodo,
                            'score':score})

    best_spots.sort(
        key=lambda item: item['score'],
        reverse=True)

    top3 = {}

    for best_spot in best_spots:

        spot_name = best_spot['name']
        score = best_spot['score']

        # If the beach is not in top3 yet, add it
        # The first score found is the best score because best_spots is already sorted
        if spot_name not in top3 and len(top3) < 3:

            top3[spot_name] = {
                'best_score': score,
                'periodos': []
            }

        # If the beach is one of top 3
        if spot_name in top3:

            best_score = top3[spot_name]['best_score']

            # Only add periods with at least 80% of the beach's best score
            if score >= best_score * 0.8:

                top3[spot_name]['periodos'].append({
                    'periodo': best_spot['periodo'],
                    'score': round(score, 2)
                })

    print(top3)

    return top3
    


"""
#=================
#SEÇÃO DO SPOTS DE SURF - FUTURAS APLICAÇÕES
#=================
#Essa rota consulta o banco de dados e devolve todas as praias cadastradas no WaveMatch
@app.route('/spots', methods=['GET'])
def get_spots():
    spots = db.session.execute(
        db.select(SurfSpot)
    ).scalars().all() # TODAS as praias - transforma o resultado em uma lista de objetos

    spots_list = []

    for spot in spots:
        spots_list.append({
            'id': spot.id,
            'name': spot.name,
            'city': spot.city,
            'state': spot.state,
            'latitude': spot.latitude,
            'longitude': spot.longitude,
            'surf_level': spot.surf_level,
            'wave_direction': spot.wave_direction,
            'predominant_direction': spot.predominant_direction,
            'wave_shape': spot.wave_shape,
            'wave_duration': spot.wave_duration,
            'wave_speed': spot.wave_speed,
            'break_length': spot.break_length,
            'current_tendency': spot.current_tendency
            })

    return jsonify(spots_list),200 


#api externa

@app.route('/spots/<int:spot_id>/forecast', methods=['GET'])
def get_forecast(spot_id): 
    spot = db.session.get(SurfSpot,spot_id)

    if spot is None:
        return jsonify({'message':'Surf Spot não encontrado'}),404

    data_marine = get_marine_data(spot)
    data_wind = get_wind_data(spot)

    wave_times = data_marine['hourly']['time']
    wave_heights = data_marine['hourly']['wave_height']
    wave_periods = data_marine['hourly']['wave_period']
    swell_wave_directions = data_marine['hourly']['swell_wave_direction']
    swell_wave_periods = data_marine['hourly']['swell_wave_period']
    wind_speeds = data_wind['hourly']['wind_speed_10m']
    wind_directions = data_wind['hourly']['wind_direction_10m']
    wind_times = data_wind['hourly']['time']


    wind_forecast = {}

    for wind_time,wind_speed_10m,wind_direction_10m in zip(wind_times,wind_speeds,wind_directions):
        wind_forecast[wind_time]={
                         'wind_speed':wind_speed_10m,
                         'wind_direction':wind_direction_10m}

    forecast = []

    for wave_time, wave_height, wave_period, swell_wave_direction, swell_wave_period in zip(wave_times, wave_heights,wave_periods,swell_wave_directions,swell_wave_periods):
        if wave_time in wind_forecast:
            wind_data = wind_forecast[wave_time]  # acessa os dados de vento correspondentes ao mesmo horário da onda

            forecast.append({'time':wave_time,
                            'wave_height':wave_height,
                            'wave_period':wave_period,
                            'swell_wave_direction':swell_wave_direction,
                            'swell_wave_period':swell_wave_period,
                            'wind_speed': wind_data['wind_speed'],
                            'wind_direction': wind_data['wind_direction']
                            })


    spot_forecast = {'spot':spot.name,
                    'forecast': forecast}
    
    
    return jsonify(spot_forecast), 200
"""


if __name__ == '__main__':
    app.run(debug=True)