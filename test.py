# coding=utf-8
import py_compile
import random

import sys

print("hello world\n" * 2)
print(2 + 3)
print('ni' + 'hao')

secret = random.randint(1, 10)
# temp = input("猜")
# guess = int(temp)

# while guess != secret:
#     temp = input("错了，重新输入吧")
#     guess = int(temp)
#     if guess == secret:
#         print("yes")
#     else:
#         print("no")

# 列表练习
number = [2, 4, 3]
number.append(9)
number.sort()
print(number)

# 列表分片
print(number[1:])

# 元组练习
tuple = (6, 5)
tuple2 = 6,
print(type(tuple2))

# 字典练习
dict = {"小鹤鹤": "大漂亮", "胖虎": "大聪明"}
for each in dict:
    print(each + " " + dict.get(each))
print(dict.keys())
print(dict)

# 集合练习
set1 = {5, 3, 2, 5}
print(set1)


def myFirstFunction(content):
    """哈哈哈
    :param content:
    :return: 打印传入值
    """
    print(content)


var = myFirstFunction.__doc__
print(var)
myFirstFunction("第一个函数")

try:
    x = 1 / 0
except ValueError:
    print("ValueError")

except:
    print("Error", sys.exc_info()[0])


def test(list):
    list = [1, 2, 3]
    print(list)


list_test = []
test(list_test)
print(list_test)
