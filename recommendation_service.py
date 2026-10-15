from datetime import datetime
from statistics import mean

from scoring_service import (
    evaluate_surf_level,
    evaluate_wave_height,
    evaluate_wind_speed,
    evaluate_wind_direction,
    mean_wind_direction
)

from weather_service import (
    get_marine_data,
    get_wind_data
)

def calculate_spot_scores(user, spot, today, min_wave_height, max_wave_height):

    # Lista para armazenar os resultados dos períodos desta praia
    period_scores = []

    # Dicionários para armazenar scores por período
    wave_heights_scores = {}
    wind_speeds_scores = {}
    wind_directions_scores = {}

    # Dicionários para armazenar valores reais por período
    wave_heights_values = {}
    wind_speeds_values = {}
    wind_directions_values = {}

    # Calcula compatibilidade entre nível do usuário e da praia
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

    # Organiza dados de vento por horário
    wind_forecast = {}

    for wind_time, wind_speed, wind_direction in zip(
        wind_times,
        wind_speeds,
        wind_directions
    ):
        if datetime.fromisoformat(wind_time).date() != today:
            continue

        wind_forecast[wind_time] = {
            'wind_speed': wind_speed,
            'wind_direction': wind_direction
        }

    # Percorre os dados de ondas e combina com os dados de vento
    for wave_time, wave_height in zip(wave_times, wave_heights):

        if wave_time not in wind_forecast:
            continue

        wind_data = wind_forecast[wave_time]
        wind_speed = wind_data['wind_speed']
        wind_direction = wind_data['wind_direction']

        hour = datetime.fromisoformat(wave_time).hour
        periodo = None

        # Identifica o período do dia
        if 5 <= hour < 8:
            periodo = 'amanhecer'

        elif 8 <= hour < 12:
            periodo = 'manhã'

        elif 12 <= hour < 16:
            periodo = 'tarde'

        elif 16 <= hour < 19:
            periodo = 'fim da tarde'

        if periodo is not None:

            # Calcula os scores de cada condição
            wave_height_score = evaluate_wave_height(
                wave_height,
                min_wave_height,
                max_wave_height
            )

            wind_speed_score = evaluate_wind_speed(wind_speed)

            wind_direction_score = evaluate_wind_direction(
                wind_direction,
                spot.beach_orientation
            )

            # Inicializa as listas do período
            if periodo not in wave_heights_scores:

                wave_heights_scores[periodo] = []
                wind_speeds_scores[periodo] = []
                wind_directions_scores[periodo] = []

                wave_heights_values[periodo] = []
                wind_speeds_values[periodo] = []
                wind_directions_values[periodo] = []

            # Armazena os scores
            wave_heights_scores[periodo].append(wave_height_score)
            wind_speeds_scores[periodo].append(wind_speed_score)
            wind_directions_scores[periodo].append(wind_direction_score)

            # Armazena os valores reais
            wave_heights_values[periodo].append(wave_height)
            wind_speeds_values[periodo].append(wind_speed)
            wind_directions_values[periodo].append(wind_direction)

    # Calcula as médias e o score final de cada período
    for periodo, scores in wave_heights_scores.items():

        wave_height_score_mean = mean(scores)
        wind_speed_score_mean = mean(wind_speeds_scores[periodo])
        wind_direction_score_mean = mean(wind_directions_scores[periodo])

        wave_height_mean = mean(wave_heights_values[periodo])
        wind_speed_mean = mean(wind_speeds_values[periodo])

        # Média circular para direções em graus
        wind_direction_mean = mean_wind_direction(
            wind_directions_values[periodo]
        )

        # Score das condições (pesos originais)
        condition_score = (
            wave_height_score_mean * 0.60
            + wind_speed_score_mean * 0.15
            + wind_direction_score_mean * 0.25
        )

        # Ajusta o score conforme o nível do surfista
        score = condition_score * level_factor

        # Adiciona o resultado do período à lista
        period_scores.append({
            'name': spot.name,
            'periodo': periodo,
            'score': score,
            'wave_height': wave_height_mean,
            'wind_speed': wind_speed_mean,
            'wind_direction': wind_direction_mean
        })

    return period_scores

def get_user_wave_preferences(user):

    # Alturas padrão conforme o nível do surfista
    default_wave_heights = {
        'iniciante': (0.4, 1.5),
        'intermediario': (0.8, 2.0),
        'avancado': (1.0, 3.0)
    }

    default_min, default_max = default_wave_heights[user.surf_level]

    min_wave_height = (
        user.min_wave_height
        if user.min_wave_height is not None
        else default_min
    )

    max_wave_height = (
        user.max_wave_height
        if user.max_wave_height is not None
        else default_max
    )

    return min_wave_height, max_wave_height