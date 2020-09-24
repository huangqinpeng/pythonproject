import pymysql as mysql
import pandas as pd
if __name__ == '__main__':
  conn = mysql.connect("localhost", "root", "root", "test", charset='utf8' )
  cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
  sql = "select cname,addr,artno,artperson,registercapital,regaddr,regtelephone from xd_sn_ccode"
  try:
    cursor.execute(sql)
    data = cursor.fetchall()
    for item in data:
      print(data.index(item),item)
    cursor.close()
    conn.close()

  except:
    print("error occurs")
  df = pd.DataFrame(data)
  writer = pd.ExcelWriter('D:/测试/客商数据.xlsx')
  df.to_excel(excel_writer=writer, sheet_name='数据', index=False, header=False)
  writer.sheets['数据'].column_dimensions['A'].width = 50
  writer.sheets['数据'].column_dimensions['B'].width = 50
  writer.sheets['数据'].column_dimensions['C'].width = 25
  writer.sheets['数据'].column_dimensions['D'].width = 10
  writer.sheets['数据'].column_dimensions['E'].width = 10
  writer.sheets['数据'].column_dimensions['F'].width = 60
  writer.sheets['数据'].column_dimensions['G'].width = 10
  writer.save()
  writer.close()


