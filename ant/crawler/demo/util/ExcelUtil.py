__author__ = 'hh'

import xlrd  as  ExcelRead
import xlwt as ExcelWrite
from datetime import datetime

class ExcelUtil():

    def buildExcel(self,name,listData,titles):
        new_workBook = ExcelWrite.Workbook()
        new_workSheet = new_workBook.add_sheet(name)
        style0 = ExcelWrite.easyxf('font: name Times New Roman, color-index red, bold on',num_format_str='#,##0.00')
        style1 = ExcelWrite.easyxf(num_format_str='D-MMM-YY')

        for i, title in enumerate(titles):
            new_workSheet.write(0,i,title)

        for j , data in enumerate(listData):
            for i, title in enumerate(titles):
                print("第%d行，第%d列的数据是%s"%(j+1,i,data[title]))
                new_workSheet.write(j+1,i,data[title])



        #new_workSheet.write(1, 0, 1234.56, style0)
        #new_workSheet.write(1, 1, datetime.now(), style1)

        #new_workSheet.write(2,0,5)
        #new_workSheet.write(2,1,8)
        #new_workSheet.write(3,0, ExcelWrite.Formula("A3+B3"))
        new_workBook.save(name+".xls")
        print("文件保存成功")

#e =   ExcelUtil()
#e.buildExcel("test",['a','a','1','1'],['a','b','c','d'])