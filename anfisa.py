import sys
from io import BytesIO
from PIL import Image
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from rita import address


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('templates/MainWindow.ui', self)
        self.scale = 3  # [0.1;7] (вообще ещё есть варианты 14 и 28, но только для схемы, т.ч. наверно нам они не нужны)
        self.run()
        self.searchBtn.clicked.connect(lambda checked, arg=True: self.run(arg))
        self.comboBox.currentTextChanged.connect(lambda checked, arg=False: self.run(arg))

    def run(self, default_scale=True):
        if default_scale:
            self.scale = 3
        search = self.inputLineEdit.text() if self.inputLineEdit.text() else 'Москва'
        layer = self.comboBox.currentText()
        img_name = 'map_img.png'
        from_address = address(search, layer.lower(), self.scale)
        img = Image.open(BytesIO(from_address[0]))
        self.fullAddressLine.setText(from_address[1])
        img.save(img_name)
        self.set_img(img_name)

    def set_img(self, img_name):
        pixmap = QPixmap(img_name)
        self.mapLabel.setPixmap(pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.scale < 7:
                if self.scale == 0.8:
                    self.scale += 0.2
                elif 1 <= self.scale:
                    self.scale += 2
                else:
                    self.scale *= 2
            self.run(False)
        elif event.key() == Qt.Key_PageDown:
            if self.scale > 0.1:
                if self.scale == 1:
                    self.scale -= 0.2
                elif 1 < self.scale <= 7:
                    self.scale -= 2
                else:
                    self.scale /= 2
            self.run(False)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
