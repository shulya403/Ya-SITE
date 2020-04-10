Составление файлов для передачи на SQL-server под генерацию графиков по ценам с шагом в месяц
Для начала по ноутбукам и мониторам

Вызывной файл - Executive.py

TTX_Clear_Data - чистит файлы  TTX покатегории. Общие преременные по категориям 
(названия папок, файлов, кодов категории) в словаре Categories в коде

MonitorClear
NotebookClear

пусковая функция класса .main()

Чистит непочищенные обновления. 
На выход TTX-file, на выход TTX-file-out в папку clrear-ttx.

SQL Insert пихает файл .xlsx в БД
tosql = FromExcelToSQL(
                 table_name,
                 file_name='TTX_files\Mth_price\Ноутбук\Concat_NB--Oct-19-Mar-20.xlsx',
                 host_name='127.0.0.1',
                 port_name=3307,
                 user_name='shulya403',
                 passwd='1qazxsw2',
                 db_name='work_shema',
                 list_exception_df_col=[] #Колонки которых нет в целевой таблице БД
                 ):
Таблица должна быто создана заранее
Еее поля (кр ID PK) должны соотв. именам в excel (пока). Лишние колонки в excel убираются через 
параметр list_exception_df_col
вызов
tosql.LetGo(begin=0, end=len(tosql.df)-1) #праметр Setep по умолчанию 10 комитит по 10 строк

Price files конкат ищет все вайлы .xlsx в теле которых есть re 'MTH-YY' и нет префикса concat
ConcatPricesExcel('TTX_files/Mth_price/Ноутбук', 'NB')
принмает на вход путь до папки и префикс категории из Enum b Categories
NBDir.ConcatenateFilesExcel()


