# TODO: Схема данных целевой СУБД
#   Базовый класс чистки
#   Класс чистки ноутбуков
#   Класс чистки мониторов
#   Конкатенация прайсов по категории по месяцам
#   Подключение к СУБД
#   Заливка в CloudSQL
#   Организация обновления данных по очистки и заливке в Clou
#   Прибить href к файлам TTX
#   дочистка NB

import pandas as pd
import numpy as np
from IPython.display import display
import re

class BaseClear(object):
# Общие функции чистки: каласс родителель для классов по отдельным категориям
# закачка фалов по категории,
# генерация целевого df c полями общими для всех категорий: Name, Vendor, Category?
# translate dict, to-int, правила

    def __init__(self):

        self.Categories = {
            'Ноутбук': {
                'url': 'https://market.yandex.ru/catalog--noutbuki/54544/list?hid=91013',
                'category': ['Ноутбук'],
                'ttx_file': 'Ноутбук--характеристики.xlsx',
                'ttx_file-out': 'NB-clear-ttx.xlsx'
            },
            'Монитор': {
                'url': 'https://market.yandex.ru/catalog--monitory/54539/list?hid=91052',
                'category': ['Монитор'],
                'ttx_file': 'Монитор--характеристики.xlsx'
            },
            'Проектор': {
                'url': 'https://market.yandex.ru/catalog--multimedia-proektory/60865/list?hid=191219',
                'category': ['Проектор',
                             'Карманный проектор'],
                'ttx_file': 'Проектор--характеристики.xlsx'
            },
            'ИБП': {
                'url': 'https://market.yandex.ru/catalog--istochniki-bespereboinogo-pitaniia/59604/list?hid=91082',
                'category': ['Интерактивный ИБП',
                             'Резервный ИБП',
                             'ИБП с двойным преобразованием'
                             ],
                'ttx_file': 'ИБП--характеристики.xlsx'
            }
        }

        self.TTX_folder = 'TTX_files/'
        self.TTX_clear_folder = 'clear_ttx/'

        self.vec_TranslateAny = np.vectorize(self.TranslateAny)

    #закачка данных на чистку
    def TTXfileRead(self, category):

        #Считываем TTX-file сырой
        filename_ttx_source = self.TTX_folder + self.Categories[category]['ttx_file']
        self.df_source = pd.read_excel(filename_ttx_source, index_col=0)

        #считываем TTX-file выходной
        filename_ttx_out = self.TTX_folder + self.TTX_clear_folder + self.Categories[category]['ttx_file-out']

        #патаемся считать ttx-file-out и выбираем на чистку только те записи из ttx-source
        # котрых нет в file-out (новопришедшие). Если такого файла нет - берем все ttx-source
        try:
            self.df_full_out = pd.read_excel(filename_ttx_out, index_col=0)

            set_source = set(self.df_source['Name'])
            set_out = set(self.df_full_out['Name'])
            set_work = set_source - set_out
            self.df_source = self.df_source[self.df_source['Name'].isin(set_work)]
            #self.df_out = self.df_basa.merge(self.df_full_out['Name'], on='Name', how='left')['Name']
        except IOError:
            pass

        self.df_out = pd.DataFrame({'Name': self.df_source['Name']})

        #display(self.df_out)
    #преобразование по словарю
 #   @np.vectorize
    def TranslateAny(self, word_, dict_):
        return dict_[word_]

    #Series unque в словарь Unique: корректировка через map_func
    def DictColumnMap(self, col_data, map_func=str()):
        dict_ = dict()
        list_col_data = list(col_data.unique())
    #    list_ = list(map(map_func, list_col_data))
        lam = lambda x: map_func(x)
        for i in list_col_data:
            dict_[i] = lam(i)

        return dict_

    def IntegerFromText(self, string):
        pattern_ = re.compile(r'\d+|[.,]')
        clear = "".join(pattern_.findall(string))

        return int(float(clear))

    #Обработчик нанов (пока просто заглушка)
    def NanProcessing(self):

        return None

class Notebook_Clear(BaseClear):
    def main(self):
        self.TTXfileRead('Ноутбук')
        
        #   ЭКРАН 'Диагональ экрана' Screen Size (SS)
        series_SS = self.df_source['Диагональ экрана']
        dict_SS = self.DictScreenSize(series_SS)
        self.df_out['Screen_size'] = self.vec_TranslateAny(series_SS, dict_SS)

        display(self.df_out)
    
    def DictScreenSize(self, col_data):
        dict_ = self.DictColumnMap(col_data, self.IntegerFromText)
        for i in dict_:
            if dict_[i] <= 12:
                dict_[i] = '<12"'
            elif dict_[i] < 16:
                dict_[i] = str(dict_[i]) + '"'
            elif dict_[i] >= 16:
                dict_[i] = "16>"
            else:
                dict_[i] = self.NanProcessing()

        print(dict_)

        return dict_

### МЭЙН
ClearNB = Notebook_Clear()
ClearNB.main()
