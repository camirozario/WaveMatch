import requests

def get_wind_data(spot):

    params_wind = {
        'latitude': spot.latitude,
        'longitude': spot.longitude,
        'hourly': 'wind_speed_10m,wind_direction_10m',
        'timezone': 'America/Sao_Paulo'
    }

    url_wind = 'https://api.open-meteo.com/v1/forecast'

    response_wind = requests.get(
        url_wind,
        params=params_wind
    )

    data_wind = response_wind.json()

    return data_wind

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