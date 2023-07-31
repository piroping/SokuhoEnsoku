from tkinter.filedialog import askopenfile
import openpyxl
import os
from collections import defaultdict


class ReadNameList:
    def __init__(self):
        self.name_list = []
    
    def open(self):
        file = askopenfile(title='名簿を指定してください', filetypes=(('Excel', '.xlsx'), ), initialdir=os.getcwd())
        if file:
            wb = openpyxl.load_workbook(file.name)
            for i in wb.sheetnames:
                di = defaultdict(int)
                year = int(i[1])
                for j in wb[i].values:
                    if j[0] == None or j[1] == None:
                        continue
                    di[j[0]] += 1
                    self.name_list.append((year, j[0], di[j[0]], j[1].strip().replace('\u200b', '').replace('\u3000', ' '))) # type: ignore
        
            return self.name_list
        exit()

if __name__ == '__main__':
    t = ReadNameList()