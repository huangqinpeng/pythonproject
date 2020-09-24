import pymssql
import  pandas  as pd
import traceback
import sys
import pymysql
#Rpt_ItmDEF_Base
mysqlcon = pymysql.connect("localhost", "root", "root", "u8_test", charset='utf8' )
mysqlcur = mysqlcon.cursor()
input=r"C:\\Users\\Huang\\Desktop\\mdm\\work.xlsx"
df = pd.read_excel(input,sheet_name = 'Sheet8')
data = df.values
data = list(data)
for d in data:
    d[0] = str(d[0]).split('(')[0][:-1]

sql= 'select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = \'xd_u8_001_inventory\''
mysqlcur.execute(sql)
newcols = mysqlcur.fetchall()
newcols = list(newcols)
newcols = eval(str(newcols).replace('(','').replace(')','').replace(',,',','))
for d in data:
    #print(d[0],d[1],d[2])
    #print(d[0])
    if(d[0] in newcols):
     if(d[2]=='bit'):
        if(str(d[1])[:5] == '存货是否有' or str(d[1])[:5] == '核算自由项' or str(d[1][:6])=='结构性自由项'):
            continue

        print('1','是','存货-' + d[1] + '-' + d[0] )
        print('0', '否', '存货-' + d[1] + '-' + d[0])
     if (d[2] == 'smallint'):
         a=0
         #print('存货-' + d[1]+ '-' + d[0])