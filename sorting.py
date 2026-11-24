import pprint

class ListCreator:
    def __init__(self, itemlist,dataInstance):
        self.itemlist = itemlist
        self.data = dataInstance
        self.FixedList = []

    def Sorter(self):
        for item in self.data.datalist:
            #make a row with item[key] where key stands for each item in self.itemlist] and item stands for each dic in datalist
            row = [item[key] for key in self.itemlist]
            self.FixedList.append(row)
        pprint.pprint(self.FixedList)