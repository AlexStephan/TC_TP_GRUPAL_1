from src.plotTool import PlotTool
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication([])
    window = PlotTool()
    window.show()
    app.exec()
