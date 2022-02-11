import sys
from io import BytesIO
import requests
from PIL import Image


def get_spn(toponym):
    frame = toponym['boundedBy']['Envelope']
    l, b = map(float, frame['lowerCorner'].split())
    u, a = map(float, frame['upperCorner'].split())

    x = abs(l - u) / 4
    y = abs(a - b) / 4

    return f'{x},{y}'


def address(toponym_to_find):
    toponym_to_find = toponym_to_find
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
        'spn': get_spn(toponym),
        'l': 'map'
    }
    map_api_server = 'http://static-maps.yandex.ru/1.x/'
    response = requests.get(map_api_server, params=map_params)

    return response.content


if __name__ == '__main__':
    ad = address('Москва, ерервинский бульвар, 14, к1')
    Image.open(BytesIO(ad)).show()