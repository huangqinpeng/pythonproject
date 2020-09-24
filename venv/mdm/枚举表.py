import pymssql
import  pandas  as pd
import traceback
import sys
input=r"C:\\Users\\Huang\\Desktop\\mdm\\work.xlsx"
df = pd.read_excel(input,sheet_name = 'Sheet8')
data = df.values
data = list(data)
connect = pymssql.connect('172.17.12.102', 'cmdmuser', 'Aa123456', 'UFMeta_001')  # 服务器名,账户,密码,数据库名
cur = connect.cursor()
sql = """select * from """ + "MetaEnumDef"
cur.execute(sql)
res = cur.fetchall()
for r in res:
    print(r)
'''
for d in data:
    sql = """select * from """ + d[0]
    cur.execute(sql)
    res = cur.fetchall()
    if(res):
        print(d[0])
        for r in res:
            print(r)
        print()
'''
