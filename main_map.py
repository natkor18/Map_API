import sys
import requests
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class MapShow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mapobj.ui', self)
        self.initUI()

    def initUI(self):
        self.searchbtn.clicked.connect(self.run)

    def run(self):
        adr, coords, spn = self.geocoder(self.address.text())
        self.file_map = 'map.png'
        with open(self.file_map, "wb") as f:
            f.write(self.map_object(coords, spn))

        self.image = QPixmap(self.file_map)
        self.label.setPixmap(self.image)

    def geocoder(self, address):
        api_server = "https://geocode-maps.yandex.ru/1.x/?"
        params = {
            "apikey": YOU_APIKEY,
            "geocode": ' '.join(address.split()),
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

    def map_object(self, coords, spn):
        api_address = "https://static-maps.yandex.ru/v1?"
        params = {
            'll': ','.join(coords.split()),
            'spn': spn,
            'pt': ','.join(coords.split()),
            'apikey': YOU_APIKEY
        }
        request_map = requests.get(api_address, params=params)
        response = request_map.content
        return response


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapShow()
    ex.show()
    sys.exit(app.exec())
