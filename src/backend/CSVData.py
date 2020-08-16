from src.backend.dataFromFile import DataFromFile
import csv

class CSVData(DataFromFile):
    def __init__(self):
        self.path = ""

    def isValid(self):
        if self.path.endswith('.csv'):
            return True
        else:
            return False

    def loadFile(self, path):
        self.path = path
        #print(self.path)

    def getNames(self):
        with open(self.path) as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            csvlist = list(data)
        return csvlist[0]

    def convert2Float(self,strlist):
        floatlist = []
        for x in strlist:
            f = float(x)
            floatlist.append(f)
        return floatlist

    def getColumnList(self, colnum):
        with open(self.path) as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            next(data, None)
            var = []
            for row in data:
                var.append(row[colnum])
        return var

    def getGraph(self):
        strvar1 = self.getColumnList(0)
        freq = self.convert2Float(strvar1)
        strvar2 = self.getColumnList(1)
        amp = self.convert2Float(strvar2)
        strvar3 = self.getColumnList(2)
        phase = self.convert2Float(strvar3)
        return freq, amp, phase

