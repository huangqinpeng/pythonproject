import pymysql
import  pandas  as pd
import  numpy   as np
db = pymysql.connect("localhost", "root", "root", "u8_test", charset='utf8' )
cursor = db.cursor()
input=r"C:\\Users\\Huang\\Desktop\\mdm\\work.xlsx"
df = pd.read_excel(input,sheet_name = 'oa重名')
data = df.values

sql = """
select id,firstrankdept
from xd_ehr_department
"""
cursor.execute(sql)
ehrmaps = cursor.fetchall()
ehrmaps = dict(ehrmaps)
#ehr name
sql = """
select id,name
from xd_ehr_department
"""
cursor.execute(sql)
ehrmaps1 = cursor.fetchall()
ehrmaps1 = dict(ehrmaps1)
sql = """
select id,parentid
from xd_ehr_department
"""
cursor.execute(sql)
ehrmaps2 = cursor.fetchall()
ehrmaps2 = dict(ehrmaps2)
#oa 部门

sql = """
select id,departmentname
from xd_oa_hrmdepartment_m
"""
cursor.execute(sql)
oamap = cursor.fetchall()
oamap = dict(oamap)



#修改为mdm的
sql = """
select oaid,ehrid
from xd_dep_link
where type = 'dep'
"""
cursor.execute(sql)
deptmaps = cursor.fetchall()
deptmaps = dict(deptmaps)
print(deptmaps)
print("oid","ehrid","oa部门id","oa部门名","人名","匹配id","匹配公司","匹配部门名","重名id","重名公司","重名部门名")
for x in data:
    if str(x[1]) in deptmaps.keys():

        ehrdeptid = deptmaps[str(x[1])]
        if(ehrdeptid != None and  ehrdeptid != '' and (not str(ehrdeptid).isspace())):
            #oa和ehr直接映射
            sql = "select * from xd_ehr_employee_m where employstatus = 110100000 and name = \"" + x[2] + "\" and deptid = \"" + ehrdeptid + "\""


            #print(sql)
            cursor.execute(sql)
            res = cursor.fetchall()
            if(len(res)!=1):          #直接搜索到
                a=0
                if(len(res)==0):#子部门
                    sql = "select * from xd_ehr_employee_m where name = \"" + x[
                        2] + "\" and deptid in (select id from xd_ehr_department where parentid = \"" + ehrdeptid + "\")"
                    #print(sql)
                    cursor.execute(sql)
                    res = cursor.fetchall()
                    if(len(res)==0):
                        a=0 #oa滞后 ehr更新 映射失效    匹配错误
                        sql = "select * from xd_ehr_employee_m where name = \"" + x[2] + "\" and employstatus = 110100000"""
                        #print(sql)
                        cursor.execute(sql)
                        res = cursor.fetchall()
                        #print("部门已匹配，出现错误，人员为", x[0], x[1], x[2])
                        #print(len(res), ehrdeptid)
                        '''for row in res:
                            a=0
                            print(x[0],row[0], x[1],oamap[x[1]], x[2],ehrdeptid,ehrmaps[ehrdeptid],ehrmaps1[ehrdeptid],row[6],ehrmaps[row[6]],ehrmaps1[row[6]])
                            if(ehrmaps2[ehrdeptid] == ehrmaps2[row[6]]):
                                print(ehrmaps2[ehrdeptid])
                        print()'''
                    else: #子部门搜索到
                        a=0
                        if(len(res)==1):
                            a=0
                            print(x[0], x[1], x[2],res[0][0],ehrdeptid, res[0][6])
                        else:
                            print("error",x[0], x[1], x[2])



            else: #直接匹配
                a=0
                print(x[0],x[1],x[2],res[0][0],ehrdeptid)
        else:
            a=0
            #print("该人员oa部门未匹配",x[0],x[1],x[2])
    else:
        a=0
        #print("该人员oa部门未匹配",x[0],x[1],x[2])

db.close()
cursor.close()