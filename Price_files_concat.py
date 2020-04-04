import os
import pandas as pd
import re
from datetime import datetime, date
from pprint import pprint

#TODO:

class ConcatPricesExcel(object):
    def __init__(self, work_folder, category):

        os.chdir(work_folder)

        self.Category = category

        self.file_list = os.listdir()
        self.xlsx_file_list = self.file_list.copy()

        self.ClearFileList()

        self.DictFileDate()

        self.list_col = ['Vendor',
                         'Name',
                         'AvgPrice',
                         'Quantaty',
                         ]


    #убирает из списка все файлы кроме xlsx, а также выходной файл 'concat'
    def ClearFileList(self):

        for i in self.file_list:
            if ('xlsx' not in i) or ('concat' in i.lower()):
                self.xlsx_file_list.remove(i)
        pprint(self.xlsx_file_list)

    #создает словарь self.dict_file_mth
    # 'файл парсов.xls': {'Mth': выражение Мес-год из имени файла, 'Date': datetaime DD-MM-YYYY}
    def DictFileDate(self):

        def toDate(re_str):

            dict_work_mth = {'Jan': 1,
                             'Feb': 2,
                             'Mar': 3,
                             'Apr': 4,
                             'May': 5,
                             'Jun': 6,
                             'Jul': 7,
                             'Aug': 8,
                             'Sep': 9,
                             'Oct': 10,
                             'Nov': 11,
                             'Dec': 12}

            date_day = 1
            date_month = dict_work_mth[re_str[:3]]
            date_year = int('20' + re_str[-2:])
            date_ = date(date_year, date_month, date_day)

            return date_

        self.dict_file_mth  = dict()
        re_M_Y = re.compile(r'[a-zA-Z]{3}-\d{2}')
        for i in self.xlsx_file_list:
            re_val = re_M_Y.search(i)
            self.dict_file_mth[i] = {'Mth': re_val.group(0),
                                     'Date': toDate(re_val.group(0))}
        pprint(self.dict_file_mth)

    #созает выходной файл concat
    def ConcatenateFilesExcel(self):

        list_date = list()

        df_concat = pd.DataFrame()
        print(df_concat)

        for i in self.dict_file_mth:
            df_work = pd.read_excel(i, usecols=self.list_col)
            date_ = self.dict_file_mth[i]['Date']
            df_work['Date'] = date_
            df_work['Category'] = self.Category
            list_date.append(date_)
            df_concat = pd.concat([df_concat, df_work])
            df_concat.reset_index()
        list_date.sort()
        begin_mth = list_date[0].strftime('%b-%y')
        end_mth = list_date[len(list_date)-1].strftime('%b-%y')
        filename_concat = 'Concat_' + self.Category + "--" + begin_mth + "-" + end_mth + ".xlsx"
        df_concat.to_excel(filename_concat)

#main

NBDir = ConcatPricesExcel('TTX_files/Mth_price/Ноутбук', 'NB')
NBDir.ConcatenateFilesExcel()
