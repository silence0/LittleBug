import re

pattern = re.compile(r'\d{3}-\d{7}-\d{7}')
orderlist = re.findall(pattern, '123-1231231-1231231a welrkjwerdf123-123-123123')
print(orderlist)