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
        print(self.path)

    def getNames(self):
        with open(self.path) as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            csvlist = list(data)
        return csvlist[0]

    def convert2Float(strlist):
        floatlist = []
        for x in strlist:
            for y in x:
                f = float(y)
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
        strvar = self.getColumnList(0)
        var1 = self.convert2Float(strvar)
        strvar = self.getColumnList(1)
        var2 = self.convert2Float(strvar)
        strvar = self.getColumnList(2)
        var3 = self.convert2Float(strvar)
        return var1, var2, var3

