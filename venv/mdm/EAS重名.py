import pymysql
import  pandas  as pd
import  numpy   as np
db = pymysql.connect("localhost", "root", "root", "u8_test", charset='utf8' )
cursor = db.cursor()
input=r"C:\\Users\\Huang\\Desktop\\mdm\\work.xlsx"
df = pd.read_excel(input,sheet_name = 'EAS重名')
data = df.values
#print(data)


sql = """
select id,name
from xd_ehr_department
"""
cursor.execute(sql)
ehrdeptmaps = cursor.fetchall()
ehrdeptmaps = dict(ehrdeptmaps)

for x in data:
    print(x[0],x[1],x[2])

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




