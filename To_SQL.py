import os
import pandas as pd
import re
from datetime import datetime
from pprint import pprint

#TODO: составить excel файлы из всех файлов в директории

class ConcatPricesExcel(object):
    def __init__(self, work_folder):
        os.chdir(work_folder)

        self.file_list = os.listdir()

    def ClearFileList(self):

        print(self.file_list)
        #re_xlsx = re.compile(r'xlsx')

        for i in self.file_list:
            if ('xlsx' not in i) or ('concat' in i.lower()):
                self.file_list.remove(i)
        print(self.file_list)

    def DictFileDate(self):

        def toDate(re_str):
            return re_str

        self.dict_file_mth = dict()
        re_M_Y = re.compile(r'[a-zA-Z]{3}-\d{2}')
        for i in self.file_list:
            re_val = re_M_Y.search(i)
            self.dict_file_mth[i] = {'Mth': re_val.group(0),
                                     'Date': toDate(re_val.group(0))}
        pprint(self.dict_file_mth)









#main

NBDir = ConcatPricesExcel('TTX_files/Mth_price/Ноутбук')
NBDir.ClearFileList()
NBDir.DictFileDate()
