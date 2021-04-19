file_name = r"C:\Users\zheng\Desktop\DimenTool2.java"
f = open(file_name, 'r', encoding='UTF-8')
print('文件的内容是：')

for each_line in f:
    print(each_line)
