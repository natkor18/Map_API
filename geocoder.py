import requests
import sys


def geocoder(address):
    api_server = "https://geocode-maps.yandex.ru/1.x/?"
    params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": address,
        "format": "json"
    }
    request_api = requests.get(api_server, params)
    response = request_api.json()
    toponym = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    toponym_address = toponym['metaDataProperty']['GeocoderMetaData']['text']
    coords = toponym['Point']['pos']

    frame_obj = toponym['boundedBy']['Envelope']
    l, b = frame_obj['lowerCorner'].split()
    r, t = frame_obj['upperCorner'].split()

    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(b) - float(t)) / 2.0
    spn = f"{dx},{dy}"
    return toponym_address, coords, spn


def map_object(coords, spn):
    api_address = "https://static-maps.yandex.ru/v1?"
    params = {
        'll': ','.join(coords.split()),
        'spn': spn,
        'pt': ','.join(coords.split()),
        'apikey': 'c37b0772-bdf0-4f65-a7e4-e8e975f896be'
    }
    request_map = requests.get(api_address, params=params)
    response = request_map.content
    return response


