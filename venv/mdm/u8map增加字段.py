import pymysql
import  pandas  as pd
import  numpy   as np
db = pymysql.connect("localhost", "root", "root", "u8_test", charset='utf8' )
cursor = db.cursor()
sql = """select * from xd_u8_ehr_dept_map"""
cursor.execute(sql)
res = cursor.fetchall()
for r in res:
    print(r[9])
    sql = """select * from xd_u8_""" + r[9][0:3] + """_Department where cDepCode = \"%s\""""%r[0]
    cursor.execute(sql)
    dept = cursor.fetchone()
    sql = "update xd_u8_ehr_dept_map set syslog = \'%s\' where u8id = \"%s\" and sysid = \'%s\' "%("U8"+r[9],r[0],r[9])
    '''if(dept[15]!= None):
        sql = "update xd_u8_ehr_dept_map set cDepName =\"%s\",iDepGrade = %s,cDepGUID = \"%s\",dDepBeginDate=\'%s\',dModifDate=\'%s\',syslog=\"U8\" where u8id = \"%s\" and sysid = \'%s\'"%(dept[2],dept[3],dept[6],dept[7],dept[15],r[0],r[9])
        #print(sql)
    else:
        sql = "update xd_u8_ehr_dept_map set cDepName =\"%s\",iDepGrade = %s,cDepGUID = \"%s\",dDepBeginDate=\'%s\',syslog=\"U8\" where u8id = \"%s\" and sysid = \'%s\'"%(dept[2],dept[3],dept[6],dept[7],r[0],r[9])
        #print(sql)'''
    print(sql)
    cursor.execute(sql)
db.commit()
