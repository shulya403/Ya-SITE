import pandas as pd
import numpy as np
from pprint import pprint
from IPython.display import display
from datetime import datetime as dt
import time

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
        self.df_src.replace(' ', 'nan', inplace=True)
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
        
        CPU_vendor__dict = self.to_dict__CPU(self.df_src['Ядро процессора'])
        self.df['CPU_Vendor'] = translate_(self.df_src['Ядро процессора'], CPU_vendor__dict )
    
    def df_show(self):
        display(self.df.head(20))
    
    def df_to_excel(self, filename, date_):
        self.df['Date'] = date_.strftime("%Y-%m-%d")
        self.df.to_excel(filename)

    def to_dict__CPU(self, series_):
        exit_ = dict()
        series_uni = series_.unique()
        CPU_ven_ = {
                'Intel': [
                        'Kaby',
                        'Ice',
                        'Comet',
                        'Broadwell',
                        'Sky',
                        'Apollo',
                        'Gemini',
                        'Whiskey',
                        'Braswell',
                        'Bay',
                        'Cherry',
                        'Amber',
                        'Coffee',
                        'Haswell',
                        'Prescott',
                        'Merom',
                        'Sandy',
                        'Silver',
                        'Arrandale',
                        'Ivy'
                        ],
                'AMD':  [
                        'Temash',
                        'Zen',
                        'Bristol',
                        'Raven',
                        'Stoney',
                        'Beema',
                        'Kabini',
                        'Carrizo',
                        'Kaveri',
                        'Pinnacle'
                        ]
                
                }
        
        exit_['nan'] = 'nan'
        
        for i in series_uni:
            if i != 'nan':
                ch = False
                for ven in CPU_ven_:
                    for platform in CPU_ven_[ven]:
                        if platform in i:
                            exit_[i] = ven
                            ch = True
                            break
                    if ch:
                        break
           
        
        return exit_
        
        
    
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
            elif series_[0] == 'nan':
                exit_.append('nan')
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
                x = 4
            else:
                x = i.find('"') - 1

            exit_[i] = i[:x]

        return exit_
    

NB = src_clear('Source/Notebook/Ноутбук-Цены11-12-19--20-28.xlsx')
NB.df_show()
date_ = dt(2019, 11, 15) #'Y19-10'

NB.df_to_excel('Exit/Notebook/Notebook_' + date_.strftime("%y-%b") + '.xlsx', date_)





