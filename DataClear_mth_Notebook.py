import pandas as pd
import numpy as np
from pprint import pprint
from IPython.display import display

class src_clear(object): #чистит исходный файл

    def __init__(self, src_file):

        @np.vectorize
        def translate_(word_, dict_):
            return dict_[word_]

        self.df_src = pd.read_excel(src_file, index_col='Name')
        del self.df_src['Unnamed: 0']
        display(self.df_src.columns)

        self.df_src = self.df_src[(self.df_src['Quantaty'] >= 2) | (self.df_src['Quantaty'] is None)]
        self.df_src.fillna('nan', inplace=True)
        print(len(self.df_src))

        self.df = pd.DataFrame(index=self.df_src.index)
        self.df['Vendor'] = self.df_src['Vendor']
        self.df['AvgPrice'] = self.df_src['AvgPrice']
        self.df['Quantaty'] = self.df_src['Quantaty']

        screen_dgn__dict = self.to_dict__screen_dgn(self.df_src['Диагональ экрана'])
        self.df['Screen diagonal'] = translate_(self.df_src['Диагональ экрана'], screen_dgn__dict)

        Sensor_ = self.df_src['Сенсорный экран'].replace('нет', False).replace('есть', True)
        self.df['Screen sensor'] = Sensor_

        #    self.df['Screen Diagonal'] = [monitor_dict[dc] for dc in self.df_src['Диагональ экрана']]

        graphics_type__dict = self.to_dict__graphics_type(self.df_src['Тип видеокарты'])
        graphics_type = translate_(self.df_src['Тип видеокарты'], graphics_type__dict)

        self.df['Graphic class'] = self.to_series__graphics_class(graphics_type, self.df_src['Видеокарта'])


    def to_series__graphics_class(self, graphics_type, videocard):

        exit_ = list()

        game_prof__ls = {
            'GTX',
            'RTX',
            'Pro',
            'Quadro',
            'RX'
        }

        for series_ in zip(graphics_type, videocard):
            if series_[0] == 'Integrated':
                exit_.append('Integrated')
            else:
                ch = False
                for j in game_prof__ls:
                    if j in series_[1]:
                        exit_.append('External Gaming/Pro')
                        ch = True
                        break
                if not ch:
                    exit_.append('External Mainstream')

        return exit_

    def to_dict__graphics_type(self, series_):
        exit_ = dict()
        series_uni = series_.unique()

        for i in series_uni:
            i = str(i)
            if 'дискретная' in i:
                exit_[i] = 'External'
            elif i == 'nan':
                exit_[i] = 'nan'
            else:
                exit_[i] = 'Integrated'

        return exit_

    def to_dict__screen_dgn(self, series_):

        exit_ = dict()
        series_uni = series_.unique()

        for i in series_uni:
            i = str(i)
            if '.' in i:
                x = i.find('.')
            elif i == 'nan':
                x = 0
            else:
                x = i.find('"') - 1

            exit_[i] = i[:x]

        return exit_

    def df_show(self):
        display(self.df.head(20))

NB = src_clear('Source/Notebook/Ноутбук-Цены25-12-19--19-50.xlsx')
NB.df_show()





