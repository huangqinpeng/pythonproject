import pymysql
import  pandas  as pd
import  numpy   as np
db = pymysql.connect("localhost", "root", "root", "u8_test", charset='utf8' )
cursor = db.cursor()
input=r"C:\\Users\\Huang\\Desktop\\mdm\\work.xlsx"
df = pd.read_excel(input,sheet_name = 'EAS重名')
data = df.values
df = pd.read_excel(input,sheet_name = 'EAS无匹配')
data1 = df.values

for x in data1:
    if(not x[0] in data[:,[0]]):
        #print(x[1],x[2])
        sql = "select * from xd_ehr_employee_m where name = \"" + x[1] + "\""""
        cursor.execute(sql)
        test = cursor.fetchall()
        if(len(test) > 1):
            print(x[1],x[2])
            for t in test:
                sql = """
                select id,name,firstrankdept,secondrankdept,thirdrankdept
                from xd_ehr_department
                where id = \"""" + t[6] + "\""
                cursor.execute(sql)
                ehrdeptmap = cursor.fetchall()
                print(t[0], "ehr", ehrdeptmap)
            #for t in test:
                #print(t[0], t[6], t[9], end="   ")
            #print("")'''
        '''if(len(test) == 1):
            if(test[0][9]=='110100001'):
                print(x[0],x[1],x[2],test[0][0],"EHR离职")
            else:
                print(x[0], x[1], x[2], test[0][0], "正常")
        if(len(test)==0):
            print(x[0],x[1],x[2],"不存在") '''
#print(data)
