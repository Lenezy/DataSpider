import xlwt

'''
workbook = xlwt.Workbook(encoding="utf-8")  # 创建workbook对象
worksheet = workbook.add_sheet('sheet1')  # 创建工作表

workbook.save('student.xls')  # 保存数据表
'''
'''
workbook = xlwt.Workbook(encoding="utf-8")  # 创建workbook对象
worksheet = workbook.add_sheet('sheet1')  # 创建工作表
for f1 in range(0, 9):
    for f2 in range(0, f1 + 1):
        worksheet.write(f1, f2,
                        "%d * %d = %d" % (f1 + 1, f2 + 1, (f1 + 1) * (f2 + 1)))  # 写入数据，第一行参数"行"，第二行参数"列"，第三个参数内容

workbook.save('student.xls')  # 保存数据表
'''