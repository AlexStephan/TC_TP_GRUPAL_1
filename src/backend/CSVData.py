from src.backend.dataFromFile import DataFromFile

class CSVData(DataFromFile):
    def __init__(self):
        self.path = ""

    def loadFile(self, path):
        self.path = path
        print(self.path)