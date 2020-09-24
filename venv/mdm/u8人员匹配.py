import pymysql
import  pandas  as pd
import  numpy   as np
db = pymysql.connect("localhost", "root", "root", "u8_test", charset='utf8' )
cursor = db.cursor()
input=r"C:\\Users\\Huang\\Desktop\\mdm\\work.xlsx"
df = pd.read_excel(input,sheet_name = 'u8人员',converters = {u'cDept_num':str})
data = df.values
#print(data)
'''
for x in data:
    sql = "select * from xd_ehr_employee_m where name = \"" + x[1] +"\""
    #print(sql)
    cursor.execute(sql)
    psn = cursor.fetchall()
    if(len(psn) == 1):
        print(psn)
'''
sql = """
select u8id ,ehrid
from xd_u8_ehr_dept_map
where sysid = '001'
"""
cursor.execute(sql)
deptmaps = cursor.fetchall()
deptmaps = dict(deptmaps)

#
sql = """
select distinct ehrid
from xd_u8_ehr_dept_map
where sysid = '001'
"""
cursor.execute(sql)
depts = cursor.fetchall()
depts = str(depts).replace('(','').replace(')','').replace(',,',',')[:-1]

for x in data:
    sql = "select * from xd_ehr_employee_m where deptid in  (" + depts + ") and name = \"" + x[1] +"\""""
    cursor.execute(sql)
    psns = cursor.fetchall()
    if(len(psns)==0):
        print("不存在",x[1],deptmaps[x[2]])
        sql = "select * from xd_ehr_employee_m where name = \"" + x[1] + "\""""
        cursor.execute(sql)
        test = cursor.fetchall()
        for t in test:
              print(t[0],t[6],t[9],end="   ")
        print()
    for psn in psns:
        if(psn[9] == '110100001'):
            a=0
            #print("EHR离职",psn[0])
        else:
            a=0
           # print("正常",psn[0])


cursor.close()
db.close()