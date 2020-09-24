import pymssql
import  pandas  as pd
import traceback
import sys
import pymysql
#Rpt_ItmDEF_Base
mysqlcon = pymysql.connect("localhost", "root", "root", "u8_test", charset='utf8' )
connect = pymssql.connect('172.17.12.102', 'cmdmuser', 'Aa123456', 'UFDATA_001_2019')  # 服务器名,账户,密码,数据库名
mysqlcur = mysqlcon.cursor()
cur = connect.cursor()
#sql= 'select * from INFORMATION_SCHEMA.COLUMNS where table_name = \'customer\''
sql= 'select * from Rpt_ItmDEF_Base where tablename = \'ua_user\''
cur.execute(sql)
res = cur.fetchall()
sql= 'select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = \'xd_u8_001_ua_user_ex\''
mysqlcur.execute(sql)
newcols = mysqlcur.fetchall()
newcols = list(newcols)
newcols = eval(str(newcols).replace('(','').replace(')','').replace(',,',','))
for col in newcols:
    print(col)
for r in res:
    print(r)

    a=0
    #if(r[0] in newcols):
        #print(r[0],r[3])
       # print(newcols.index(r[0]))
    #print(res.index(r),r)
        #if(r[4] == 'bit'):
            #print('1','是','供应商-'+ r[3] + '-' +r[0])
           # print('0','否','供应商-'+ r[3] + '-' +r[0])'''


cur.close()
mysqlcur.close()
connect.close()
mysqlcon.close()