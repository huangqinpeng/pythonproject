import difflib
import pymysql
db = pymysql.connect("localhost", "root", "root", "u8_test", charset='utf8' )

depTable = "xd_u8_167_department"
coname = "\"深圳市灏天光电有限公司\""
def get_equal_rate(str1, str2):
   return difflib.SequenceMatcher(None, str1, str2).quick_ratio()
def match(res,ehrDep,dep):
    #if(dep[2] ==1):
    t = get_equal_rate(ehrDep[1], dep[1])
        #t = get_equal_rate(ehrDep[1], str(dep[3]).split('/')[1])
    if (t > res[0]):
        res = [round(t,2), dep[0],dep[3],ehrDep[0], ehrDep[1]]
    return res

cursor = db.cursor()
sql = """
select cDepCode,cDepName,iDepGrade,cDepFullName
 from """ + depTable
cursor.execute(sql)
deps = cursor.fetchall()
#print(deps)


sql = """select id,name,deptlevel,parentid from xd_ehr_department where thirdrankdept = """ + coname
#print(sql)
cursor.execute(sql)
ehrDeps = cursor.fetchall()
#print(ehrDeps)
for ehr in ehrDeps:
    print(ehr[0],ehr[1],ehr[2],ehr[3])
for dep in deps:
    res = [0,"未匹配的部门:" + dep[1]]
    rate = 0
    for ehrDep in ehrDeps:
        if(dep[2] == 1):
            if(len(ehrDep[2])==8):
                res = match(res,ehrDep,dep)

        else:
            if(len(ehrDep[2]) >= 8):
                a=0
                res = match(res, ehrDep, dep)

    if(len(res)>3):
        a=0
        print(res[0],res[1],res[2],res[3],res[4])
    else:
        a=0
        print(dep[0],dep[3])