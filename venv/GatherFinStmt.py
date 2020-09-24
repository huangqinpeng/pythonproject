#汇总预算报表
from os import path
from os import listdir
from os import system
import xlwings as xw
import traceback
import copy as copy
import configparser

config = configparser.ConfigParser()    # 注意大小写
config.read("配置文件.ini",encoding="UTF-8")
configArgs = config['info']
sum_file_name = configArgs['汇总表文件名']

current_path = path.abspath('.')
sum_excel_path = path.join(current_path,sum_file_name)  #汇总表路径
current_path += configArgs['板块文件夹']
co_list = eval(configArgs['板块排序'])    #板块排序
#资产负债表参数 复制来源范围
PLS_range_str1 = configArgs['资产复制表范围1']
PLS_range_str2 = configArgs['资产复制表范围2']
#利润表参数  复制来源范围
BS_range_str1 = configArgs['利润表范围1']
BS_range_str2 = configArgs['利润表范围2']
#现金流量表参数  复制来源范围
CFS_range_str1 = configArgs['现金流量表范围1']
CFS_range_str2 = configArgs['现金流量表范围2']
title_color = eval(configArgs['标题颜色'])



def range_copy(range_from,range_to):
    #xlwings range复制 包括数据，列宽，颜色
    range_to.value = range_from.value
    for i in range(range_from.columns.count):
        range_to.columns[i].column_width = range_from.columns[i].column_width  #列宽
        for j in range(range_from.rows.count):   #逐个单元格复制格式
            Cell_to = range_to.columns[i].rows[j]
            Cell_from = range_from.columns[i].rows[j]
            Cell_to.color = Cell_from.color
            Cell_to.api.HorizontalAlignment = Cell_from.api.HorizontalAlignment
            Cell_to.api.Font.Name = Cell_from.api.Font.Name
            Cell_to.api.Font.Size = Cell_from.api.Font.Size
            Cell_to.api.Font.Color = Cell_from.api.Font.Color
            Cell_to.api.NumberFormat = Cell_from.api.NumberFormat
            Cell_to.api.Borders(7).LineStyle = Cell_from.api.Borders(7).LineStyle
            Cell_to.api.Borders(8).LineStyle = Cell_from.api.Borders(8).LineStyle
            Cell_to.api.Borders(9).LineStyle = Cell_from.api.Borders(9).LineStyle
            Cell_to.api.Borders(10).LineStyle = Cell_from.api.Borders(10).LineStyle

            #Cell_to.api.Font.Color = Cell_from.api.Font.Color

def merge_cells(range,value):  #合并表头单元格并赋值
    range.value = value
    range.api.HorizontalAlignment = -4108
    range.api.Merge()
    range.color = title_color
    range.api.Borders(7).LineStyle = 1
    range.api.Borders(8).LineStyle = 1
    range.api.Borders(9).LineStyle = 1
    range.api.Borders(10).LineStyle = 1

sequence = list(map(lambda x: chr(x), range(ord('A'), ord('Z') + 1)))
def column_to_name(colnum):  #26进制转10进制 数字转excel列名
    colnum -= 1
    L = []
    if colnum > 25:
        while True:
            d = int(colnum / 26)
            remainder = colnum % 26
            if d <= 25:
                L.insert(0, sequence[remainder])
                L.insert(0, sequence[d - 1])
                break
            else:
                L.insert(0, sequence[remainder])
                colnum = d - 1
    else:
        L.append(sequence[colnum])
    return "".join(L)

def summary():
 #汇总功能  主要功能
 try:
    app = xw.App(visible=False, add_book=False)
    app.display_alerts = False
    app.screen_updating = False
    wb_sum = app.books.open(sum_excel_path)     #打开汇总表
    #资产负债表相关参数   变动数公式插入位置
    assets_change_cols = []    #资产变动数 列 数组
    liabilities_change_cols = []    #负债变动数 列 数组

    ##############################################################
    if (configArgs['是否复制利润表'] == '是'):
        to_range = wb_sum.sheets[configArgs['利润表汇总工作表']].range(
            BS_range_str1[0:3] + chr(ord(BS_range_str1[3]) + 2) + BS_range_str1[4:6])  # 汇总表格范围 固定 根据模板
        for index in range(to_range.rows.count):  # 擦除汇总表的原公式 如果存在
            if (index == 0):      #跳过表头
                continue
            else:
                to_range.rows[index].clear_contents()
    ##############################################################
    if (configArgs['是否复制现金流量表'] == '是'):
        to_range = wb_sum.sheets["现金流量表汇总底稿"].range(
            CFS_range_str1[0:3] + chr(ord(CFS_range_str1[3]) + 2) + CFS_range_str1[4:6])  # 汇总表格范围 固定 根据模板
        for index in range(to_range.rows.count):  # 清除汇总表的原公式 如果存在
            if (index == 0):      #跳过表头
                continue
            else:
                to_range.rows[index].clear_contents()
    ##############################################################

    files = listdir(current_path)  #各板块文件
    for f in files:
        if(f.startswith('~') or f.split('.')[-1] != 'xlsx'):    #去除excel打开后的临时文件
            files.remove(f)
    files = sorted(files, key=lambda x: co_list.index(x.split('-')[-1].split('.')[0]))    #根据板块列表co_list排序
    for f in files:
        co_name = f.split('-')[-1].split('.')[0]  #公司名 需要规范文件名
        wb_cur = app.books.open(path.join(current_path, f))
        print('打开：' + f)

        #资产复制表复制
        if(configArgs['是否复制资产负债表'] == '是'):
            copy_PLS(wb_sum,wb_cur,assets_change_cols,liabilities_change_cols,co_name)
        #利润表复制
        if (configArgs['是否复制利润表'] == '是'):
            copy_BS(wb_sum,wb_cur,co_name)
        #现金流量表复制
        if (configArgs['是否复制现金流量表'] == '是'):
            copy_CFS(wb_sum, wb_cur, co_name)
        wb_cur.close()
    if (configArgs['是否复制资产负债表'] == '是'):
        build_PLS_formulas(wb_sum.sheets[configArgs['资产负债表汇总工作表']], assets_change_cols, liabilities_change_cols)  #一次性写入公式
    wb_sum.save()
    wb_sum.close()
    app.quit()
 except Exception as ex:
    traceback.print_exc()
    app.quit()

# 资产复制表复制
def copy_PLS(wb_sum,wb_cur,assets_change_cols,liabilities_change_cols,co_name):
    work_sheet = wb_sum.sheets[configArgs['资产负债表汇总工作表']]
    current_copy_col_num = work_sheet.used_range.last_cell.column  # 汇总excel 资产复制表当前最右端列
    # 注意 这是数据复制前的值
    # 构建表头   高度耦合
    title_range_1_str = column_to_name(current_copy_col_num + 1) + '2' + ':' + column_to_name(
        current_copy_col_num + 6) + '2'
    title_range_1 = work_sheet.range(title_range_1_str)
    merge_cells(title_range_1, co_name)
    title_range_2_str = column_to_name(current_copy_col_num + 1) + '3' + ':' + column_to_name(
        current_copy_col_num + 3) + '3'
    title_range_2 = work_sheet.range(title_range_2_str)
    merge_cells(title_range_2, "资产")
    assets_change_cols.append(column_to_name(current_copy_col_num + 2))  # 资产变动数的列号
    title_range_3_str = column_to_name(current_copy_col_num + 4) + '3' + ':' + column_to_name(
        current_copy_col_num + 6) + '3'
    title_range_3 = work_sheet.range(title_range_3_str)
    merge_cells(title_range_3, "负债及所有者权益")
    liabilities_change_cols.append(column_to_name(current_copy_col_num + 5))  # 负债变动数的列号
    # 复制数据
    copy_to_range_str = column_to_name(current_copy_col_num + 1) + PLS_range_str1[1] + ':' + column_to_name(
        current_copy_col_num + 3) + PLS_range_str1[4:6]
    copy_from = wb_cur.sheets['资产负债表'].range(PLS_range_str1)  # 资产负债表  资产数据位置 固定
    copy_to = work_sheet.range(copy_to_range_str)  # 汇总表
    range_copy(copy_from, copy_to)
    copy_to_range_str = column_to_name(current_copy_col_num + 4) + PLS_range_str1[1] + ':' + column_to_name(
        current_copy_col_num + 6) + PLS_range_str1[4:6]
    copy_from = wb_cur.sheets['资产负债表'].range(PLS_range_str2)  # 资产负债表  负债，所有数据位置 固定
    copy_to = work_sheet.range(copy_to_range_str)  # 汇总表
    range_copy(copy_from, copy_to)
    print(co_name + '资产负债表复制完成')

def build_PLS_formulas(sheet,assets_change_cols,liabilities_change_cols):
    #构建汇总表公式 资产负债表   注意不覆盖原有合计公式 流动资产总计等
    try:
        assets_change_range = sheet.range(configArgs['资产变动数范围'])
        liabilities_change_range = sheet.range(configArgs['负债变动数范围'])
        for i in range(assets_change_range.rows.count):
            formula_str = '='
            for col_name in assets_change_cols:
                formula_str = formula_str + col_name + str(assets_change_range.row + i) + '+'
            assets_change_range.rows[i].formula = formula_str[:len(formula_str)-1]

        for i in range(liabilities_change_range.rows.count):
            formula_str = '='
            for col_name in liabilities_change_cols:
                formula_str = formula_str + col_name + str(assets_change_range.row + i) + '+'
            liabilities_change_range.rows[i].formula = formula_str[:len(formula_str)-1]
        print("资产负债表写入公式")
    except Exception as ex:
        traceback.print_exc()

#利润表复制
def copy_BS(wb_sum,wb_cur,co_name):
    sum_sheet = wb_sum.sheets[configArgs['利润表汇总工作表']]
    current_copy_col_num = sum_sheet.used_range.last_cell.column  # 汇总excel 利润表当前最右端
    cols_num = ord(BS_range_str1[3]) - ord(BS_range_str1[0]) + 1  # 月份实际数、预测数 列的数目
    #构建表头
    title_range_str = column_to_name(current_copy_col_num + 2) + '3' + ':' + column_to_name(current_copy_col_num + cols_num + 3) + '3'
    title_range = sum_sheet.range(title_range_str)
    merge_cells(title_range, co_name)
    # 复制数据
    copy_to_range_str = column_to_name(current_copy_col_num + 2) + BS_range_str1[1] + ':' + column_to_name(
        current_copy_col_num + cols_num + 1) + BS_range_str1[4:6]
    copy_from = wb_cur.sheets["利润表"].range(BS_range_str1)
    copy_to = sum_sheet.range(copy_to_range_str)  # 汇总表
    range_copy(copy_from, copy_to)
    copy_to_range_str = column_to_name(current_copy_col_num + cols_num + 2) + BS_range_str1[1] + ':' + column_to_name(
        current_copy_col_num + cols_num + 3) + BS_range_str2[4:6]
    copy_from = wb_cur.sheets["利润表"].range(BS_range_str2)
    copy_to = sum_sheet.range(copy_to_range_str)  # 汇总表
    range_copy(copy_from, copy_to)

    build_BS_formulas(sum_sheet)
    wb_sum.save()
    print(co_name + '利润表复制完成')

def build_BS_formulas(sum_sheet):
    # 构建汇总表公式 利润表
    #在之前的函数清除原公式
    try:
        current_col_num = sum_sheet.used_range.last_cell.column  # 汇总excel 表当前最右端
        cols_num = ord(BS_range_str1[3]) - ord(BS_range_str1[0]) + 3   #模板列数 与to_range.rows.count - 1 一致
        to_range = sum_sheet.range(BS_range_str1[0:3] + chr(ord(BS_range_str1[3]) + 2) + BS_range_str1[4:6])  #汇总表格范围 固定 根据模板
        ##assets_change_range.rows[i].formula = formula_str[:len(formula_str) - 1]
        begin_col = current_col_num - cols_num + 1   #公式构造  最后一个复制表起始列
        begin_row = to_range.row + 1  #起始行修正1，汇总表
        filter_col = []
        filter_row = []
        for i in range(to_range.columns.count):
            for j in range(to_range.rows.count - 1):  #修正
                #print(column_to_name(i+2),j +5,to_range.columns[i].rows[j + 1].formula)
                #print(to_range.cols[i].rows[j].address,to_range.columns[i].rows[j + 1].formula)
                if(to_range.columns[i].rows[j+1].formula==''):
                    to_range.columns[i].rows[j+1].formula = '=' + column_to_name(begin_col + i) + str(j + 5)
                else:
                    to_range.columns[i].rows[j + 1].formula += ('+' + column_to_name(begin_col + i) + str(j + 5))
                #print(column_to_name(begin_col + i) + str(begin_row + j))
        print("利润表写入公式")
    except Exception as ex:
        traceback.print_exc()  #可能要抛出异常

def copy_CFS(wb_sum,wb_cur,co_name):
    sum_sheet = wb_sum.sheets[configArgs['现金流量表汇总工作表']]
    current_copy_col_num = sum_sheet.used_range.last_cell.column  # 汇总excel 现金流量表当前最右端
    cols_num = ord(CFS_range_str1[3]) - ord(CFS_range_str1[0]) + 1  # 月份实际数、预测数 列的数目
    #构建表头
    title_range_str = column_to_name(current_copy_col_num + 2) + '3' + ':' + column_to_name(current_copy_col_num + cols_num + 3) + '3'
    title_range = sum_sheet.range(title_range_str)
    merge_cells(title_range, co_name)
    # 复制数据
    copy_to_range_str = column_to_name(current_copy_col_num + 2) + CFS_range_str1[1] + ':' + column_to_name(
        current_copy_col_num + cols_num + 1) + CFS_range_str1[4:6]
    copy_from = wb_cur.sheets["现金流量表"].range(CFS_range_str1)
    copy_to = sum_sheet.range(copy_to_range_str)  # 汇总表
    range_copy(copy_from, copy_to)
    copy_to_range_str = column_to_name(current_copy_col_num + cols_num + 2) + CFS_range_str1[1] + ':' + column_to_name(
        current_copy_col_num + cols_num + 3) + CFS_range_str1[4:6]
    copy_from = wb_cur.sheets["现金流量表"].range(CFS_range_str2)
    copy_to = sum_sheet.range(copy_to_range_str)  # 汇总表
    range_copy(copy_from, copy_to)
    build_CFS_formulas(sum_sheet)
    wb_sum.save()
    print(co_name + '现金流量表复制完成')

def build_CFS_formulas(sum_sheet):
    # 构建汇总表公式 现金流量表   注意不覆盖原有合计公式
    #在之前的函数清除原公式
    try:
        current_col_num = sum_sheet.used_range.last_cell.column  # 汇总excel 表当前最右端
        cols_num = ord(CFS_range_str1[3]) - ord(CFS_range_str1[0]) + 3   #模板列数 与to_range.rows.count - 1 一致
        to_range = sum_sheet.range(CFS_range_str1[0:3] + chr(ord(CFS_range_str1[3]) + 2) + CFS_range_str1[4:6])  #汇总表格范围 固定 根据模板
        ##assets_change_range.rows[i].formula = formula_str[:len(formula_str) - 1]
        begin_col = current_col_num - cols_num + 1   #公式构造  最后一个复制表起始列
        begin_row = to_range.row + 1  #起始行修正1，汇总表
        filter_col = []
        filter_row = []
        for i in range(to_range.columns.count):
            for j in range(to_range.rows.count - 1):  #修正
                #print(column_to_name(i+2),j +5,to_range.columns[i].rows[j + 1].formula)
                #print(to_range.cols[i].rows[j].address,to_range.columns[i].rows[j + 1].formula)
                if(to_range.columns[i].rows[j+1].formula==''):
                    to_range.columns[i].rows[j+1].formula = '=' + column_to_name(begin_col + i) + str(j + 5)
                else:
                    to_range.columns[i].rows[j + 1].formula += ('+' + column_to_name(begin_col + i) + str(j + 5))
                #print(column_to_name(begin_col + i) + str(begin_row + j))
        print("现金流量表写入公式")
    except Exception as ex:
        traceback.print_exc()  #可能要抛出异常


if __name__ == '__main__':
    summary()
    #print(sum_file_name)
    input()