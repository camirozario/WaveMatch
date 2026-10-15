import math

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


def evaluate_wind_direction(wind_direction, beach_orientation):

    difference = abs(wind_direction - beach_orientation)

    if difference > 180:
        difference = 360 - difference

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

def mean_wind_direction(directions):

    sin_sum = sum(math.sin(math.radians(d)) for d in directions)
    cos_sum = sum(math.cos(math.radians(d)) for d in directions)

    angle = math.degrees(math.atan2(sin_sum, cos_sum))

    return angle % 360


def wind_direction_to_compass(degrees):

    directions = [
        "N", "NE", "E", "SE",
        "S", "SW", "W", "NW"
    ]

    index = round(degrees / 45) % 8

    return directions[index]

def classify_wind_direction(wind_direction, beach_orientation):

    difference = abs(wind_direction - beach_orientation)

    if difference > 180:
        difference = 360 - difference

    if difference <= 30:
        return "Onshore"

    elif difference <= 60:
        return "Side-onshore"

    elif difference <= 120:
        return "Cross-shore"

    elif difference <= 150:
        return "Side-offshore"

    else:
        return "Offshore"


def evaluate_wave_height(wave_height, min_wave_height, max_wave_height):

    ideal_wave_height = (min_wave_height + max_wave_height) / 2

    if wave_height == ideal_wave_height:
        return 100

    elif wave_height == min_wave_height:
        return 50

    elif wave_height == max_wave_height:
        return 50

    elif min_wave_height < wave_height < ideal_wave_height:
        return round(
            100 - abs(wave_height - ideal_wave_height)
            / abs(ideal_wave_height - min_wave_height) * 50, 2
        )

    elif ideal_wave_height < wave_height < max_wave_height:
        return round(
            100 - abs(wave_height - ideal_wave_height)
            / abs(ideal_wave_height - max_wave_height) * 50, 2
        )

    elif wave_height < min_wave_height:
        score = 50 - abs(min_wave_height - wave_height) / abs(
            ideal_wave_height - min_wave_height
        ) * 50

        return round(max(0, score), 2)

    elif wave_height > max_wave_height:
        score = 50 - abs(max_wave_height - wave_height) / abs(
            ideal_wave_height - max_wave_height
        ) * 50

        return round(max(0, score), 2)



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
    

