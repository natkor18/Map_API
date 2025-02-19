import sys
import requests
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from geocoder import geocoder, map_object


class MapShow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mapobj.ui', self)
        self.initUI()

    def initUI(self):
        self.zoom = 5
        self.searchbtn.clicked.connect(self.run)

    def run(self):
        self.update_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp and self.zoom < 20:
            self.zoom += 1
            self.update_map()
        if event.key() == Qt.Key.Key_PageDown and self.zoom > 1:
            self.zoom -= 1
            self.update_map()

    def update_map(self):
        self.adr, self.coords, self.spn = geocoder(self.address.text())
        self.file_map = 'map.png'

        api_address = "https://static-maps.yandex.ru/v1?"
        params = {
            "ll": ','.join(self.coords.split()),
            "z": f"{self.zoom}",
            "pt": ','.join(self.coords.split()),
            'apikey': YOU_APIKEY
        }
        sessia = requests.Session()
        sessia_map = sessia.get(api_address, params=params)

        with open(self.file_map, "wb") as f:
            f.write(sessia_map.content)

        self.image = QPixmap(self.file_map)
        self.label.setPixmap(self.image)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapShow()
    ex.show()
    sys.exit(app.exec())