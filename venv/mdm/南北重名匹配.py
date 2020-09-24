import pymysql
import  pandas  as pd
import  numpy   as np
db = pymysql.connect("localhost", "root", "root", "u8_test", charset='utf8' )
cursor = db.cursor()
input=r"C:\\Users\\Huang\\Desktop\\mdm\\work.xlsx"
df = pd.read_excel(input,sheet_name = '南北重名')
data = df.values
#print(data)
sql = """
select id,bname
from xd_sn_bcode_m
"""
cursor.execute(sql)
deptmaps = cursor.fetchall()
deptmaps = dict(deptmaps)

sql = """
select id,bname
from xd_sn_bcode_m
"""
cursor.execute(sql)
deptmaps = cursor.fetchall()
deptmaps = dict(deptmaps)
sql = """
select id,name
from xd_ehr_department
"""
cursor.execute(sql)
ehrdeptmaps = cursor.fetchall()
ehrdeptmaps = dict(ehrdeptmaps)

for x in data:
    print(x[0],x[1])
    sql = "select * from xd_sn_bcode_m where wcode = \"" + x[0] + "\""""
    cursor.execute(sql)
    bs = cursor.fetchall()
    for b in bs:
        print (b[0][:11],deptmaps[b[0][:11]])
    sql = "select * from xd_ehr_employee_m where employstatus = 110100000 and name = \"" + x[1] + "\""
    cursor.execute(sql)
    psns = cursor.fetchall()
    for psn in psns:
        sql = """
        select id,name,firstrankdept,secondrankdept,thirdrankdept
        from xd_ehr_department
        where id = \"""" + psn[6] +"\""
        cursor.execute(sql)
        ehrdeptmap = cursor.fetchall()
        print(psn[0],"ehr",ehrdeptmap)
    print()




