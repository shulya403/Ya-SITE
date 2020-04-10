# TODO: ok Схема данных целевой СУБД
#   ok Базовый класс чистки
#   ok Класс чистки ноутбуков
#   ok Класс чистки мониторов
#   0k Конкатенация прайсов по категории по месяцам
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
# translate dict, column-to-dict, to-int, и т. п.

    def __init__(self):

        self.Categories = {
            'Ноутбук': {
                'url': 'https://market.yandex.ru/catalog--noutbuki/54544/list?hid=91013',
                'category': ['Ноутбук'],
                'ttx_file': 'Ноутбук--характеристики.xlsx',
                'ttx_file_out': 'NB-clear-ttx.xlsx',
                'out_name': 'NB'
            },
            'Монитор': {
                'url': 'https://market.yandex.ru/catalog--monitory/54539/list?hid=91052',
                'category': ['Монитор'],
                'ttx_file': 'Монитор--характеристики.xlsx',
                'ttx_file_out': 'MNT-clear-ttx.xlsx',
                'out_name': 'MNT'
            },
            'Проектор': {
                'url': 'https://market.yandex.ru/catalog--multimedia-proektory/60865/list?hid=191219',
                'category': ['Проектор',
                             'Карманный проектор'],
                'ttx_file': 'Проектор--характеристики.xlsx',
                'out_name': 'PRT'
            },
            'ИБП': {
                'url': 'https://market.yandex.ru/catalog--istochniki-bespereboinogo-pitaniia/59604/list?hid=91082',
                'category': ['Интерактивный ИБП',
                             'Резервный ИБП',
                             'ИБП с двойным преобразованием'
                             ],
                'ttx_file': 'ИБП--характеристики.xlsx',
                'out_name': 'UPS'
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

        #патаемся считать ttx-file-out и выбираем на чистку только те записи из ttx-source
        # котрых нет в file-out (новопришедшие). Если такого файла нет - берем все ttx-source
        try:
            # считываем TTX-file выходной
            self.filename_ttx_out = self.TTX_folder + self.TTX_clear_folder + self.Categories[category]['ttx_file-out']
            self.df_full_out = pd.read_excel(self.filename_ttx_out, index_col=0)

            set_source = set(self.df_source['Name'])
            set_out = set(self.df_full_out['Name'])
            set_work = set_source - set_out
            self.df_source = self.df_source[self.df_source['Name'].isin(set_work)]

        except Exception:
            self.filename_ttx_out = ''
            self.df_full_out = pd.DataFrame()

        self.df_source.fillna('nan', inplace=True)
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

        lam = lambda x: map_func(x)
        for i in list_col_data:
            dict_[i] = lam(i)

        return dict_

    #Берет из str только цифры и ./, преобразовывает float в int
    def IntegerFromText(self, string):
        pattern_ = re.compile(r'\d+|[.,]')
        print(string)
        if string == 'nan':
            clear = string
        else:
            clear = "".join(pattern_.findall(string))
            clear = int(float(clear))

        return clear

    #присваивает ключ словаря 'key': {набор значений} при нахождении одного из значений в строке для unique;
    #если не находит ни одго значения примваивает alter_word
    def DictColumnSetPresent(self, col_data, dict_set_words, alter_word):

        dict_ = dict()

        for i in col_data.unique():
            if str(i) == 'nan':
                h_val = None
            else:
                h_val = alter_word
                for src_val in dict_set_words:
                    for token in dict_set_words[src_val]:
                        if token.lower() in i.lower():
                            h_val = src_val
                            break
                    if h_val != alter_word:
                        break
            dict_[i] = h_val

        return dict_

    #Обработчик нанов (пока просто заглушка)
    def NanProcessing(self):

        return None
    #добавлят данные df_out к архиву (ели он есть) или формирует первичный архив
    def DFOuttoExcel(self, category):

        if self.filename_ttx_out == '':
            filename = self.TTX_folder + self.TTX_clear_folder + self.Categories[category]['ttx_file_out']
            self.df_out.to_excel(filename)
        else:
            df_last_data = pd.read_excel(self.filename_ttx_out, index_col=0)
            df_last_data = pd.concat([df_last_data, self.df_out])
            df_last_data.to_excel(self.filename_ttx_out)


class NotebookClear(BaseClear):
    def main(self):
        self.TTXfileRead('Ноутбук')
        
        #   ЭКРАН 'Диагональ экрана' Screen Size (SS)
        series_SS = self.df_source['Диагональ экрана']
        dict_SS = self.DictScreenSize(series_SS)
        self.df_out['Screen_size'] = self.vec_TranslateAny(series_SS, dict_SS)

        # ГРАФИКА ТИП 'Тип видеокарты' Video
        series_video_type = self.df_source['Тип видеокарты']
        series_GPU = self.df_source['Видеокарта']
        self.df_out['Video_conf'] = self.CdVideo(series_video_type, series_GPU).values

        #КЛАСТЕРЫ Экран, 'Тип видеокарты'
        self.df_out['Clusters_Screen/GPU'] = 'None'
        self.df_out.loc[self.df_out['Screen_size'] == '<12"', 'Clusters_Screen/GPU'] = 'Mini (<12")'
        self.df_out.loc[self.df_out['Screen_size'].isin({'13"', '14"'}), 'Clusters_Screen/GPU'] = 'Thin (13"-14")'
        self.df_out.loc[self.df_out['Video_conf'] == 'External Pro', 'Clusters_Screen/GPU'] = 'Prof. WS'
        self.df_out.loc[(self.df_out['Video_conf'] == 'External GM')
                        & (self.df_out['Screen_size'].isin({'15"', '16">'})), 'Clusters_Screen/GPU'] = 'Gamer GPU (15">)'
        self.df_out.loc[(self.df_out['Video_conf'] == 'External MS')
                        & (self.df_out['Screen_size'].isin({'15"', '16">'})), 'Clusters_Screen/GPU'] = 'Ex. Mainstream GPU (15">)'
        self.df_out.loc[(self.df_out['Video_conf'] == 'Integrated')
                        & (self.df_out['Screen_size'].isin({'15"', '16">'})), 'Clusters_Screen/GPU'] = 'Integrated GPU (15">)'

        display(self.df_out.head(10))

        self.DFOuttoExcel('Ноутбук')

    def CdVideo(self, cd_video_type, cd_GPU):
        dictsf_video_type = {
            'External': {'дискретная'},
            'nan': {'nan'}
        }

        dictsf_GPU_class = {
            'GM': {'GTX', 'RTX', 'RX', 'R7'},
            'Pro': {'Quadro', 'FirePro', 'Pro WX'},
            'nan': {'nan'}
        }

        dict_video_type = self.DictColumnSetPresent(cd_video_type, dictsf_video_type, 'Integrated')
        dict_GPU_External = self.DictColumnSetPresent(cd_GPU, dictsf_GPU_class, 'MS')

        df_wrk = pd.DataFrame({'video_type': self.vec_TranslateAny(cd_video_type, dict_video_type),
                               'GPU': self.vec_TranslateAny(cd_GPU, dict_GPU_External)})
        #display(df_wrk)
        df_wrk.loc[df_wrk['video_type'] == 'Integrated', 'GPU'] = 'Int'
        #display(df_wrk)
        df_wrk['Video_conf'] = None
        df_wrk.loc[df_wrk['video_type'] == 'Integrated', 'Video_conf'] = 'Integrated'
        df_wrk.loc[df_wrk['GPU'] != 'Int', 'Video_conf'] = df_wrk['video_type'] + ' ' + df_wrk['GPU']
        #display(df_wrk)

        return df_wrk['Video_conf']

    def DictScreenSize(self, col_data):
        dict_ = self.DictColumnMap(col_data, self.IntegerFromText)
        for i in dict_:
            if dict_[i] == 'nan':
                dict_[i] = self.NanProcessing()
            elif dict_[i] <= 12:
                dict_[i] = '<12"'
            elif dict_[i] < 16:
                dict_[i] = str(dict_[i]) + '"'
            elif dict_[i] >= 16:
                dict_[i] = '16">'
            else:
                dict_[i] = self.NanProcessing()

        print(dict_)

        return dict_


class MonitorClear(BaseClear):
    def main(self):
        self.TTXfileRead('Монитор')

        #   ЭКРАН 'Диагональ экрана' Screen Size (SS)
        series_SS = self.df_source['Диагональ']
        dict_SS = self.DictScreenSize(series_SS)
        self.df_out['Screen_size'] = self.vec_TranslateAny(series_SS, dict_SS)

        #display(self.df_out)
        self.DFOuttoExcel('Монитор')

    def DictScreenSize(self, col_data):
        dict_ = self.DictColumnMap(col_data, self.IntegerFromText)
        for i in dict_:

            if dict_[i] == 'nan':
                dict_[i] = self.NanProcessing()
            elif dict_[i] <= 19:
                dict_[i] = '<19"'
            elif dict_[i] < 34:
                dict_[i] = str(dict_[i]) + '"'
            elif dict_[i] >= 34:
                dict_[i] = "34>"
            else:
                dict_[i] = self.NanProcessing()

        print(dict_)

        return dict_


### МЭЙН
#ClearNB = NotebookClear()
#ClearNB.main()

#ClearMonitor = MonitorClear()
#ClearMonitor.main()

