import TTX_Clear_Data as cl
import SQL_Insert as sq
import Price_files_concat as concat

#Составляем файл с ценами по месяцам
#MNTDir = concat.ConcatPricesExcel('TTX_files/Mth_price/Монитор', 'MNT')
#MNTDir.ConcatenateFilesExcel()


#Дополнение TTX

#запрвляем в MySQL
#C:\Users\shulya403\Shulya403_works\Ya-SITE\TTX_files\Mth_price\Монитор


tosql = sq.FromExcelToSQL(table_name='prices',
                          file_name='TTX_files\Mth_price\Монитор\Concat_MNT--Jan-20-Feb-20.xlsx',
                          list_exception_df_col=['Unnamed: 0'])
tosql.LetGo(begin=0, end=len(tosql.df)-1)
