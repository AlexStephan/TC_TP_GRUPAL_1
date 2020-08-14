from src.myWidget import MyWidget
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication([])
    window = MyWidget()
    window.show()
    app.exec()
