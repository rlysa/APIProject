import sys
from io import BytesIO
from PIL import Image
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from rita import address


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('templates/MainWindow.ui', self)
        self.set_img('data/yandex_maps')
        self.searchBtn.clicked.connect(self.run)

    def run(self):
        search = self.inputLineEdit.text()
        layer = self.comboBox.currentText()
        img_name = 'map_img.png'
        img = Image.open(BytesIO(address(search, layer.lower())))
        img.save(img_name)
        self.set_img(img_name)

    def set_img(self, img_name):
        pixmap = QPixmap(img_name)
        self.mapLabel.setPixmap(pixmap)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
