import pandas as pd
import pymysql
from pprint import pprint
import re

#TODO:
#
# зарядить всю БД

class FromExcelToSQL(object):

    def __init__(self,
                 table_name,
                 file_name='TTX_files\Mth_price\Ноутбук\Concat_NB--Oct-19-Mar-20.xlsx',
                 host_name='127.0.0.1',
                 port_name=3307,
                 user_name='shulya403',
                 passwd='1qazxsw2',
                 db_name='work_shema',
                 list_exception_df_col=[]
                 ):

        self.df = pd.read_excel(file_name)

        #Connection
        self.connection = pymysql.connect(host=host_name, port=port_name, user=user_name, password=passwd, db=db_name)
        self.curs = self.connection.cursor()


        self.table_name = table_name
        self.db_name = db_name

        self.dbt_name = "`{}`.`{}`".format(self.db_name, self.table_name)

        self.fetch_db_table_fields = self.dbtShowFields(self.dbt_name)
        pprint(self.fetch_db_table_fields)

        self.fields_OK = False
        self.dict_fields = self.FieldsTodict(list_exception_df_col)
        pprint(self.dict_fields)

    #Формирует словарь 'поле df из файла: {соотв поле из db, его тип, допустимость нанов}
    def FieldsTodict(self, except_df_col=[]):

        col_df = list(self.df.columns)
        print(col_df, type(col_df))

        for excp in except_df_col:
            col_df.remove(excp)

        dict_fields = dict()
        for i in col_df:
            dict_fields[i] = self.GetDBFields(i)

        #Нашлись ли все поля?
        list_not_ok = list()

        list_not_ok = [i for i in dict_fields if dict_fields[i]['db_field'] == '']
        print(list_not_ok)
        if list_not_ok == []:
            self.fields_OK = True
        else:
            print("Несовпадающие поля в df: ", list_not_ok)
            raise
            # TODO: здесь по идее обработчик переназначения имен полей если они не совпаают с полями таблицы базы
            #  или выкидывание лишних

        #проверить поля
        for i in dict_fields:
            self.dfCorrection(dict_fields[i])
            print(i, self.df[i].dtypes)

        return dict_fields

    #приводит типы df в соответсвии с типами целевых полей db
    def dfCorrection(self, dict_field):

        no_num = re.compile(r'[\D]+')
        dbf_ = dict_field['db_field']

        df_col_type = str(self.df[dbf_].dtypes)

        #float_to_int
        if 'int' in dict_field['ftype'].lower():
            if 'float' in df_col_type:
                try:
                    self.df[dbf_] = self.df[dbf_].astype('int32')
                except ValueError:
                    print("возможно NaN в цифровом поле {}".format(dbf_))
                    raise
            elif 'object' in df_col_type:
                print("какая-то херня в поле типа int {}".format(dbf_))
                raise
                #print(self.df[self.df[dbf_].str.contains('\D', na=True, regex=True)])
                #self.df.drop(self.df[self.df[dbf_].str.match(r'[\D]+')].index, inplace=True)

        #enum
        elif 'enum' in dict_field['ftype'].lower():
            list_enum = dict_field['ftype'][5:-1].replace(" '",'').replace("'", '').split(",")

            set_df_enum_col = set(self.df[dbf_].unique()) - {'None', 'na'}
            if not set_df_enum_col.issubset(set(list_enum)):
                print("В поле {} есть значения не из enum: ".format(dbf_), (set_df_enum_col ^ set(list_enum)) - set(list_enum))
                raise
        #NaN
        if not dict_field['none']:
            if self.df[dbf_].isnull().any():
                print("В Not Null поле {} есть Null: ".format(dbf_))
                raise

    # возвращает словарь db_field: db_ftype: db_none
    def GetDBFields(self, df_col_name):

        dict_ = {'db_field': "",
                 'ftype': "",
                 'none': True}
        for i in self.fetch_db_table_fields:
            if i[0] == df_col_name:
                dict_['db_field'] = i[0]
                dict_['ftype'] = i[1]
                if i[2] == 'YES':
                    dict_['none'] = True
                elif i[2] == 'NO':
                    dict_['none'] = False

        return dict_


    #self.fetch_db_table_fields - возврат сервера с columns database.table
    def dbtShowFields(self, dbt_name):

        self.curs.execute("SHOW COLUMNS FROM {}".format(dbt_name))

        return self.curs.fetchall()

    def ConClose(self):
        self.curs.close()
        self.connection.close()

    #вормирует str запроса SQL INSERT INTO
    def Query(self, df_row):

        sql_begin = "INSERT INTO {} ".format(self.dbt_name)

        pull_ = "("
        tup_fields_name = list()
        tup_values = list()

        for i in self.dict_fields:
            pull_ += "{}" + ", "


            tup_fields_name.append("`{}`".format(self.dict_fields[i]['db_field']))
            tup_values.append("'{}'".format(df_row[i]))
        pull_ = pull_[:-2] + ')'
        sql_values = pull_.format(*tuple(tup_fields_name)) + ' VALUES ' + pull_.format(*tuple(tup_values))

        return sql_begin + sql_values

    def LetGo(self, begin=0, end=1, step=10):

        offset = begin
        off_tail = int(end % step)
        while offset + off_tail <= end:
            if (end - offset) // step >= 1:
                lag = step
            else:
                lag = off_tail + 1

            for i in range(offset, offset + lag):
                print(self.Query(self.df.iloc[i]))
                self.curs.execute(self.Query(self.df.iloc[i]))

            self.connection.commit()
            offset += step
            print(offset)

    #теcтинг без записи
    def LetTest(self):

        for i in range(len(self.df)-1):
            print(self.Query(self.df.iloc[i]))





#tosql = FromExcelToSQL(table_name='prices', file_name='TTX_files\Mth_price\Ноутбук\Concat_mistakes.xlsx')
#tosql = FromExcelToSQL(table_name='mnt',
#                       file_name='TTX_files\clear_ttx\MNT-clear-ttx.xlsx',
#                       list_exception_df_col=['Unnamed: 0'])

#tosql.LetGo(begin=0, end=len(tosql.df)-1)

#tosql.ConClose()







