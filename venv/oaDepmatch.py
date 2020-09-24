import difflib
import pymysql
import numpy as np
db = pymysql.connect("localhost", "root", "root", "u8_test", charset='utf8' )
#db = pymysql.connect("172.16.19.153", "root", "Xindeco123", "mdm_centre", charset='utf8' )

comTable = "xd_oa_hrmsubcompany_m"
depTable = "xd_oa_hrmdepartment_m"

def get_equal_rate(str1, str2):
   return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

def match(res,ehrDep,dep):

    t = get_equal_rate(ehrDep[1], dep[1])
    if (t > res[0]):
        res = [round(t,2), dep[0],dep[1],ehrDep[0], ehrDep[1]]
    return res

def find(id,deps):
    for dep in deps:
        if(dep[0] == id):
            return dep
cursor = db.cursor()


sql = """
select oid,ehrid
from xd_oa_ehr_dept_map
"""
cursor.execute(sql)
deptmaps = cursor.fetchall()
deptmaps = dict(deptmaps)



sql = """
select id,departmentname,subcompanyid1,supdepid
from xd_oa_hrmdepartment_m
"""
cursor.execute(sql)
deps = cursor.fetchall()
deps1 = list(deps)
print(deps1)
for dep in deps1:
    deps1[deps1.index(dep)] = list(dep)

print(deps1)




sql = """select id,deptlevel from xd_ehr_department"""
cursor.execute(sql)
ehrDepmaps = cursor.fetchall()
ehrDepmaps = dict(ehrDepmaps)

for dep in deps1:
    ehrid = ''
    res = [0, "未匹配部门 ：" + dep[1]]
    if(int(dep[2]) in deptmaps.keys()):
        ehrid = deptmaps[int(dep[2])]
    if(not ehrid.isspace() and ehrid !=''):
        ehrdeptlevel = ehrDepmaps[ehrid]

        #print(ehrdeptlevel)
        sql = """
        select id,name ,deptlevel from xd_ehr_department
        where deptlevel like 
        \"""" + ehrdeptlevel + "%\""
        cursor.execute(sql)
        ehrtdeps = cursor.fetchall()
        for  ehrDep in ehrtdeps:
            res = match(res, ehrDep, dep)
            if (ehrDep[2] == ehrdeptlevel):
                com = ehrDep[1]

        if(len(res)>3):
            a = 0
            #print(res[0], com, res[1], res[2], res[3], res[4])
        else:
            a=0
            #print(com,dep[0],dep[1])
    else:
        a=0
        sql = """
        select *
        from xd_oa_ehr_dept_map
        where oid = 
        """ + dep[2]
        cursor.execute(sql)
        com = cursor.fetchone()
        if(com == None):
            print(dep[0],dep[1],dep[2])
        else:
            print(dep[0],dep[1],dep[2],com[1])



'''

for dep in deps1:
    res = [0,"未匹配部门 ："+ dep[1]]
    ehrid = deptmaps[dep[]]
    for ehrDep in ehrDeps1:
        res = match(res,ehrDep,dep)
    print(res[0],res[1],res[2],res[3],res[4])
'''

cursor.close()
db.cursor()