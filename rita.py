import requests


def get_spn(toponym, scale):
    frame = toponym['boundedBy']['Envelope']
    l, b = map(float, frame['lowerCorner'].split())
    u, a = map(float, frame['upperCorner'].split())

    x = abs(l - u) / scale
    y = abs(a - b) / scale

    return f'{x},{y}'


def get_layer(layer):
    if layer == 'схема':
        return 'map'
    elif layer == 'спутник':
        return 'sat'
    elif layer == 'гибрид':
        return 'sat,skl'


def address(toponym_to_find, layer='схема', scale=3):
    geocoder_api_server = 'http://geocode-maps.yandex.ru/1.x/'
    geocoder_params = {
        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
        'geocode': toponym_to_find,
        'format': 'json'}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        pass

    json_response = response.json()
    toponym = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    toponym_coodrinates = toponym['Point']['pos']
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(' ')

    map_params = {
        'll': ','.join([toponym_longitude, toponym_lattitude]),
        'spn': get_spn(toponym, scale),
        'l': get_layer(layer)
    }
    map_api_server = 'http://static-maps.yandex.ru/1.x/'
    response = requests.get(map_api_server, params=map_params)

    full_address = toponym['metaDataProperty']['GeocoderMetaData']['text']

    return response.content, full_address