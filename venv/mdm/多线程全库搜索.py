#!/usr/bin/python
# -*- coding=utf-8 -*-
import time
import threading
import pymssql
import  pandas  as pd
import sys
import traceback
import queue
from DBUtils.PooledDB import PooledDB
input=r"C:\\Users\\Huang\\Desktop\\mdm\\work.xlsx"
df = pd.read_excel(input,sheet_name = 'Sheet7')
tables = df.values
tables = list(tables)
finalres =[]

def mysql_connection():
    host = '172.17.12.102'
    user = 'cmdmuser'
    port = 1433
    password = 'Aa123456'
    db = 'UFDATA_001_2019'
    charset = 'utf8'
    limit_count = 3  # 最低预启动数据库连接数量
    pool = PooledDB(pymssql, limit_count, maxconnections=15, host=host, user=user, port=port, password=password, database=db,
                    charset=charset)
    return pool


def tread_connection_db(index,tablename):
   try:
    print("处理表",index,tablename)
    if (index == 1551):
        print("测试")
    con = pool.connection()
    cur = con.cursor()
    sql = '''select column_name,data_type from INFORMATION_SCHEMA.COLUMNS where table_name = %s'''
    cur.execute(sql,tablename)
    cols = cur.fetchall()
    time.sleep(0.1)
    if(index == 1515):
        print("测试",cols)
    for col in cols:
        if(col[1] != 'nvarchar'):
            continue
        sql = "select * from " + tablename + " where " + col[0] +  " = \'是否成交\' """
        cur.execute(sql, (tablename,col[0]))
        res = cur.fetchone()
        time.sleep(0.1)
        if(res):
            finalres.append([tablename,res])
            print("存在结果!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            sys.exit(0)


    con.close()
   except:

       print("出错",sql)

if __name__ == '__main__':
   try:
    start = time.time()
    # 创建线程连接池，最大限制15个连接
    pool = mysql_connection()
    q = queue.Queue(maxsize=1)
    # 测试数据，多线程查询数据库
    for table in tables:
        tread_connection_db(tables.index(table),table[0])
    print(finalres)

    ''' time.sleep(0.02)
        # 创建线程并放入队列中
        t = threading.Thread(target=tread_connection_db, args=(tables.index(table),table[0],))
        q.put(t)
        # 队列队满
        if q.qsize() == 10:
            # 用于记录线程，便于终止线程
            join_thread = []
            # 从对列取出线程并开始线程，直到队列为空
            while q.empty() != True:
                t = q.get()
                join_thread.append(t)
                t.start()
            # 终止上一次队满时里面的所有线程
            for t in join_thread:
                t.join()
    end = time.time() - start
    print(end)'''

   except:
     traceback.print_exc()
     a = 0