import pymssql
import  pandas  as pd
import traceback
import sys


connect = pymssql.connect('172.17.12.102', 'cmdmuser', 'Aa123456', 'UFDATA_003_2019')  # 服务器名,账户,密码,数据库名
cur = connect.cursor()
sql = '''select * from INFORMATION_SCHEMA.TABLES'''
cur.execute(sql)
cols = cur.fetchall()
print(len(cols))