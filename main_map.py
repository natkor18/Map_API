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
        self.searchbtn.clicked.connect(self.run)

    def run(self):
        adr, coords, spn = geocoder(self.address.text())
        self.file_map = 'map.png'
        with open(self.file_map, "wb") as f:
            f.write(map_object(coords, spn))

        self.image = QPixmap(self.file_map)
        self.label.setPixmap(self.image)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapShow()
    ex.show()
    sys.exit(app.exec())