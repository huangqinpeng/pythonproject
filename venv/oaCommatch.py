import difflib
import pymysql
#db = pymysql.connect("localhost", "root", "root", "u8_test", charset='utf8' )
db = pymysql.connect("172.16.19.153", "root", "Xindeco123", "mdm_centre", charset='utf8' )

depTable = "xd_oa_hrmsubcompany_m"

def get_equal_rate(str1, str2):
   return difflib.SequenceMatcher(None, str1, str2).quick_ratio()
def match(res,ehrDep,dep):
    t = get_equal_rate(ehrDep[1], dep[1])
    if (t > res[0]):
        res = [round(t,2), dep[0],dep[1],ehrDep[0], ehrDep[1]]
    return res

cursor = db.cursor()
sql = """
select id,subcompanydesc
 from """ + depTable
cursor.execute(sql)
deps = cursor.fetchall()
print(deps)


sql = """select id,name,deptlevel from xd_ehr_department where orgtypename = '公司'"""
#print(sql)
cursor.execute(sql)
ehrDeps = cursor.fetchall()
print(ehrDeps)


for dep in deps:
    res = [0,"未匹配单位："+ dep[1]]
    for ehrDep in ehrDeps:
        res = match(res,ehrDep,dep)
    print(res[0],res[1],res[2],res[3],res[4])
'''
for dep in deps:
    res = [0,"未匹配的部门:" + dep[1]]
    rate = 0
    for ehrDep in ehrDeps:
        if(dep[2] == 1):
            if(len(ehrDep[2])==6):
                res = match(res,ehrDep,dep)
        elif (dep[2] == 2):
            if (len(ehrDep[2]) == 8):
                res = match(res,ehrDep,dep)
        elif (dep[2] == 3):
            if (len(ehrDep[2]) == 10):
                res = match(res,ehrDep,dep)
        elif (dep[2] == 4):
            if (len(ehrDep[2]) >= 10):
                res = match(res,ehrDep,dep)
        elif (dep[2] == 5):
            if (len(ehrDep[2]) >= 12):
                res = match(res, ehrDep, dep)
    print(res)'''

cursor.close()
db.cursor()