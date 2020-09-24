import pymssql
import  pandas  as pd
import traceback
import sys

connect = pymssql.connect('172.17.12.102', 'cmdmuser', 'Aa123456', 'UFDATA_001_2019')  # 服务器名,账户,密码,数据库名
cur = connect.cursor()
sql = "select * from hr_sys_itemdict_Base where ctablecode = " + "\'Vendor\'"
print(sql)
cur.execute(sql)
res = cur.fetchall()
print(res)
for r in res:
    print('{}'.format(r))
    #print(r[1],r[2])
    if(r[5]!='' and r[5]!=None and r[5]!='<NULL>'):
        #print(r[1],r[2],end=" ")
        tablename = r[5]
        sql = 'select * from %s'%tablename
        cur.execute(sql)
        dicts = cur.fetchall()
        for d in dicts:
            a=0
            #print(r[1],r[2],d[0],d[1])
            print(d[0], d[1], "客户-" +r[2] +'-'+ r[1])
            #print(d[0])
    else:
        if(r[4]==6):
            a=0

            #print(1,"是","客户-"+r[2]+"-"+r[1])
            #print(0, "否", "客户-" + r[2] + "-" + r[1])



cur.close()
connect.close()