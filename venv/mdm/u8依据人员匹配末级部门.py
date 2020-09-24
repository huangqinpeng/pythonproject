import difflib
import pymysql
db = pymysql.connect("localhost", "root", "root", "u8_test", charset='utf8' )

depTable = "xd_u8_167_department"
cursor = db.cursor()
sql = """
select cDepCode,cDepFullName
 from """ + depTable
cursor.execute(sql)
depts = cursor.fetchall()
depts = dict(depts)

sql = """select id,name from xd_ehr_department """
cursor.execute(sql)
ehrDeps = cursor.fetchall()
ehrDeps = dict(ehrDeps)

#print(ehrDeps)
sql = """select cPsn_Name, cDept_num from xd_u8_167_hr_hi_person """
cursor.execute(sql)
perdept = cursor.fetchall()
perdept = dict(perdept)
for per in perdept.keys():
    sql = """select deptid from xd_ehr_employee_m where name = \"%s\""""%per
    cursor.execute(sql)
    res = cursor.fetchall()
    if(len(res)==1):
        print(perdept[per],depts[perdept[per]],res[0][0],ehrDeps[res[0][0]])
    elif(len(res)>1):
        print("重名")
        for r in res:
            print(perdept[per], depts[perdept[per]], res[0][0], ehrDeps[res[0][0]])
    else:
        print("未找到:",per)
    print()


