import pandas as pd
import pymysql

#TODO: Загнать connect внутрь класса
# сделать словарь пересеченией df и полей целевой БД
# переделать запрос в форму: поле=value
# сделть LetGo с офсетом
#зарядить всю БД

class FromExcelToSQL(object):

    def __init__(self,
                 table_name,
                 file_name='TTX_files\Mth_price\Ноутбук\Concat_NB--Oct-19-Mar-20.xlsx',
                 host_name='127.0.0.1',
                 port_name=3307,
                 user_name='shulya403',
                 passwd='1qazxsw2',
                 db_name='work_shema'
                 ):

        self.df = pd.read_excel(file_name)

        #Connection
        self.connection = pymysql.connect(host=host_name, port=port_name, user=user_name, password=passwd, db=db_name)
        self.curs = self.connection.cursor()


        self.table_name = table_name
        self.db_name = db_name

        self.dbt_name = "`{}`.`{}`".format(self.db_name, self.table_name)
        print(self.dbt_name)
        self.db_fields = self.dbtShowFields(self.dbt_name)

        #fields_dict

        self.dfCorrection() #float -> int

    def FieldsTodict(self, except_df_col):

        col_df = self.df.columns


        return {}


    def ConClose(self):
        self.curs.close()
        self.connection.close()

    def dbtShowFields(self, dbt_name):

        self.curs.execute("SHOW COLUMNS FROM {}".format(dbt_name))
        list_fetch = self.curs.fetchall()
        return list_fetch

    def Query(self, df_row):

        #df_row = self.df.iloc[0]

        sql_begin = "INSERT INTO `{0}`.`{1}` ".format(self.db_name,  self.tbl_name)

        fiel_ns = "("
        for i in range(len(self.fields)-1):
            fiel_ns += "`{" + str(i) + "}`" + ", "
        fiel_ns += "`{" + str(len(self.fields)-1) + "}`) "

        sql_fields = sql_begin + fiel_ns.format(*tuple(self.fields))

        value_ns = "("
        for i in range(len(df_row)-1):
            value_ns += "'{" + str(i) + "}'" + ", "
        value_ns += "'{" + str(len(df_row)-1) + "}')"

        tup_values = tuple([df_row[i] for i in self.fields])
        sql_values = sql_fields + 'VALUES' + value_ns.format(*tup_values) +';'

        return sql_values

    def dfCorrection(self):


     #       for i in self.df.columns:
    #
     #           if self.df[i].dtypes.name == 'float64':
      #              self.df[i] =self.df[i].astype('int32')


    def LetGo(self, begin, end):

        for i in range(begin, end+1):
            SQL_query = self.Query(self.df.iloc[i])
            print(SQL_query)
            self.cursor.execute(SQL_query)
            connection.commit()


tosql = FromExcelToSQL(table_name='prices')
#tosql.LetGo(0,2)

tosql.ConClose()







