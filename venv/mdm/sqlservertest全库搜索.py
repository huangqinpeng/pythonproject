import pymssql
import  pandas  as pd
import traceback
import sys
input=r"C:\\Users\\Huang\\Desktop\\mdm\\work.xlsx"
df = pd.read_excel(input,sheet_name = 'Sheet6')
data = df.values
data = list(data)
connect = pymssql.connect('172.17.12.102', 'cmdmuser', 'Aa123456', 'UFDATA_001_2019')  # 服务器名,账户,密码,数据库名
cur = connect.cursor()
finalres = []
for d in data:
     try:
        index = data.index(d)
        sql = '''select column_name,data_type from INFORMATION_SCHEMA.COLUMNS where table_name = %s'''
        cur.execute(sql,d[0])
        cols = cur.fetchall()
        if(len(cols) < 15):
            for col in cols:
                if(col[1] != 'nvarchar'):
                    continue
                sql = "select * from " + d[0] + " where " + col[0] +  " = \'0101030103\' """

                cur.execute(sql)
                res = cur.fetchone()
                if(res):
                    finalres.append([d[0],res])
                    print("存在结果!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" ,d[0])
                    #sys.exit(0)
     except:
         #traceback.print_exc()
         print("表格",index,d[0],"无法正常查找")
print(finalres)
'''
for d in data:
     sql = "SELECT max(ordinal_position) FROM INFORMATION_SCHEMA.COLUMNS where table_name = %s"
     cur.execute(sql,(d[0]))
     res = cur.fetchall()
     if(res[0][0]<=10):
         print(d[0])

cur.close()
connect.close()
'''
'''
SELECT max(ordinal_position) FROM INFORMATION_SCHEMA.COLUMNS
where table_name = 'tc_survey'
'''