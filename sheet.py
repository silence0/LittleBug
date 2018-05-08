# -*- coding: utf-8 -*-
import xlwt

book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('test', cell_overwrite_ok=True)

sheet.write(0, 0, 'currentThreadSenderId')  # 其中的'0-行, 0-列'指定表中的单元，'currentThreadSenderId'是向该单元写入的内容
sheet.write(0, 1, 'orderId')
txt1 = '中文名字'
sheet.write(1, 0, txt1)  # 此处需要将中文字符串解码成unicode码，否则会报错
txt2 = '马可瓦多'
sheet.write(1, 1, txt2)
 
# 最后，将以上操作保存到指定的Excel文件中
book.save(r'/Users/djc/Desktop/test1.xls')  # 在字符串前加r，声明为raw字符串，这样就不会处理其中的转义了。否则，可能会报错