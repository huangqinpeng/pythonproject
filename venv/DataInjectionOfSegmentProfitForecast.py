#分部门利润预测表数据注入
import  pandas  as pd
import  numpy   as np
import os
from openpyxl import load_workbook
import configparser
#excel 列字母 to num
def colname_to_num(colname):
    if type(colname) is not str:
        return colname
    col = 0
    power = 1
    for i in range(len(colname)-1,-1,-1):
        ch = colname[i]
        col += (ord(ch)-ord('A')+1)*power
        power *= 26
    return col - 1 #数组修正量
#读取配置
config = configparser.ConfigParser()    # 注意大小写
config.read("config.ini",encoding="UTF-8")
configArgs = config['info']
#读表
input = configArgs['inputFileName']
output = configArgs['outputFileName']
func = int(configArgs['function'])
inputSheetName = configArgs['inputSheetName']
df = pd.read_excel(input,sheet_name = inputSheetName)
inputBegin = int(configArgs['inputBegin'])
inputEnd = int(configArgs['inputEnd'])
if(inputEnd == 0):
    data = df.values[inputBegin : ] #读取第n行开始
else:
    data = df.values[inputBegin : inputEnd]

deptCol = colname_to_num(configArgs['deptCol'])
balanceCol = colname_to_num(configArgs['balanceCol']) #默认余额在后
data = data[:,[deptCol,balanceCol]] #读取哪几列
data = data.tolist()

delDepts = eval(configArgs['delDepts'])
replaceDepts = eval(configArgs['replaceDepts'])
gmRatio = eval(configArgs['gmRatio'])
#生成部门数据
for row in data[:]:
    #print(row[0])
    s = row[0]  #替换成deptcol
    sp = s.split("-")
    for delDept in delDepts :    #明细账数据删除逻辑
        if (sp[0] == delDept[0] and sp[1] == delDept[1]):
            index = data.index(row)
            del data[index]
            continue;
    row.remove(row[0])
    if(len(sp)==3):
        row.insert(0,'')
    else:
        row.insert(0,sp[3])
    row.insert(0,sp[2])
    for replaceDept in replaceDepts: #明细账数组 部门替换逻辑
        if(sp[0] == replaceDept[0] and sp[1] == replaceDept[1]):
            sp[0] = replaceDept[2]
            sp[1] = replaceDept[3]
    row.insert(0,sp[1])
    row.insert(0,sp[0])
    if(func == 3):
        gmBalance = row[-1] * gmRatio[sp[0]] #归母系数根据中心
        row.append(gmBalance)
#生成部门sheet
deptDf = pd.DataFrame(data)
if(func == 3):
    deptDf.columns = ['公司','部门','品种','项目','净利润','归母净利润']
elif(func == 2):
    deptDf.columns = ['公司', '部门', '品种', '项目', '余额']
else:
    deptDf.columns = ['公司', '部门', '品种', '项目', '营业收入']
#增加计算归母利润
writer = pd.ExcelWriter(input)
book = load_workbook(input)   #读取你要写入的workbook
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book)
deptDf.to_excel(excel_writer=writer, sheet_name='部门',index=False, header=True)
writer.sheets['部门'].column_dimensions['A'].width = 30
writer.sheets['部门'].column_dimensions['B'].width = 30
writer.sheets['部门'].column_dimensions['C'].width = 30
writer.sheets['部门'].column_dimensions['D'].width = 30
writer.sheets['部门'].column_dimensions['E'].width = 20
if(func == 3):
    writer.sheets['部门'].column_dimensions['F'].width = 20
writer.save()
writer.close()
print('部门表已写入')

#根据部门第一次计算
#增加归母利润计算
sumData = {} #部门利润合计 字典
sumData1 = {} #归母利润合计
for i in range(len(data)):
    dept = data[i][1]
    if(not dept in sumData):
        if(i == len(data)-1):  #最后一行
            sumData.update({dept : data[i][4]}) #index of data
            if(func == 3):
                sumData1.update({dept: data[i][5]})  # index of data
        else:
            sumData.update({dept : data[i][4]})
            if (func == 3):
                sumData1.update({dept: data[i][5]})
            for j in range(i+1 ,len(data)):
                if(data[j][1] == dept):
                    sumData[dept] += data[j][4]
                    if (func == 3):
                        sumData1[dept] += data[j][5]
#print("获取到所有的值:\n{0}".format(sumData))#格式化输出
#print("{0}".format(data))
if(func == 3):
    Datalist = zip(list(sumData.keys()),list(sumData.values()),list(sumData1.values()))
else:
    Datalist = zip(list(sumData.keys()), list(sumData.values()))
deptDf = pd.DataFrame(Datalist)
writer = pd.ExcelWriter(input)
book = load_workbook(input)   #读取你要写入的workbook
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book)
deptDf.to_excel(excel_writer=writer, sheet_name='部门合计',index=False, header=False)
writer.sheets['部门合计'].column_dimensions['A'].width = 30
writer.sheets['部门合计'].column_dimensions['B'].width = 30
if(func == 3):
    writer.sheets['部门合计'].column_dimensions['C'].width = 30
writer.save()
writer.close()
print('部门合计表已写入')

outputSheetName = configArgs['outputSheetName']
df = pd.read_excel(output,sheet_name=outputSheetName)
wb = load_workbook(filename=output)  # 打开excel文件
ws = wb[outputSheetName]
print('打开利润预测表')
#print(df.columns)
dept = df.loc[:,'   2   0   2   0  年 全年 年 度 利   润   预   测']
deptmap = eval(configArgs['deptmap'])
#插入数据到利润分析表
dept = dept.tolist()
insertBlanceCol = configArgs['insertBlanceCol']
insertgmBlanceCol = configArgs['insertgmBlanceCol']
divNum = float(configArgs['divNum'])
for ix in sumData.keys():
    if (ix in deptmap): #匹配具有优先级
        index = dept.index(deptmap[ix])
        BlanceCol = insertBlanceCol + str(index + 2) #合并单元格修正量 2
        if (func == 3):
            gmBlanceCol = insertgmBlanceCol + str(index + 2)
        ws[BlanceCol] = sumData[ix] / divNum
        if (func == 3):
            ws[gmBlanceCol] = sumData1[ix] / divNum
        continue
    elif(ix in dept):   #部门名一致
        index = dept.index(ix)
        BlanceCol = insertBlanceCol + str(index + 2)
        if (func == 3):
            gmBlanceCol = insertgmBlanceCol + str(index + 2)
        ws[BlanceCol] = sumData[ix] / divNum
        if (func == 3):
            ws[gmBlanceCol] = sumData1[ix] / divNum
        continue
    else:
        index = dept.index('其他')
        BlanceCol = insertBlanceCol + str(index + 2)
        if (func == 3):
            gmBlanceCol = insertgmBlanceCol + str(index + 2)
        ws[BlanceCol].value = str(ws[BlanceCol].value)

        if(not ws[BlanceCol].value.isspace() and ws[BlanceCol].value!= 'None'):
            ws[BlanceCol] = float(ws[BlanceCol].value) + sumData[ix] / divNum
        else:
            ws[BlanceCol] = sumData[ix] / divNum
        if (func == 3):
            ws[gmBlanceCol].value = str(ws[gmBlanceCol].value)
            if(not ws[gmBlanceCol].value.isspace() and ws[gmBlanceCol].value!='None'):
                ws[gmBlanceCol] = float(ws[gmBlanceCol].value) + sumData1[ix] / divNum
            else:
                ws[gmBlanceCol] = sumData1[ix] / divNum
wb.save(output)

print('利润表（分部门）写入\n程序结束')