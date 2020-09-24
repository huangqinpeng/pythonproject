import pymysql
db = pymysql.connect("localhost", "root", "root", "u8_test", charset='utf8' )
#db = pymysql.connect("172.16.19.153", "root", "Xindeco123", "mdm_centre", charset='utf8' )

# 使用cursor()方法获取操作游标
cursor = db.cursor()
table = "xd_u8_001_UTU_User"
# 使用execute方法执行SQL语句
sql1 = """
select column_name 
from information_schema.columns 
where table_name='""" + table + """'"""
cursor.execute(sql1)
# 使用 fetchone() 方法获取一条数据
data = cursor.fetchall()
n=0
for d in data:
    sql2 = """select count(*) from """ + table + " where " + str(d)[2:-3] +" is not null"
    cursor.execute(sql2)
    num = cursor.fetchone()
    #print(sql2)
    #print(num)
    #if(int(str(num[1:2])) == 0):
    if(int(str(num)[1:-2]) != 0):
        print(str(d)[2:-3])
        n+=1
print(n)
cursor.close()
# 关闭数据库连接
db.close()