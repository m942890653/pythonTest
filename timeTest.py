import calendar
import time

ticks = time.time()
print("当前时间戳为:", int(ticks))

# 获取格式化的时间
localtime = time.asctime(time.localtime(time.time()))
print("本地时间为 :", localtime)

# 格式化成2016-03-20 11:45:39形式
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# 将格式字符串转换为时间戳
a = "Sat Mar 28 22:24:24 2016"
print(time.mktime(time.strptime(a, "%a %b %d %H:%M:%S %Y")))

cal = calendar.month(2018, 3)
print("以下输出2018年3月份的日历:")
print(cal)