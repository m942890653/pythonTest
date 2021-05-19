# coding=utf-8
# @author: zheng
# @date:   2021/5/19 14:00
# 解析apk信息。支持双击py文件和将apk拖到py文件上两种方式
import os
import sys

apkFilePath = None  # apk文件全路径
if len(sys.argv) == 1:
    print("sys.argv[0]: " + sys.argv[0])
    versionInfo = sys.version_info
    print(sys.version_info)
    print(u"请输入apk文件全路径或用鼠标拖入")
    if versionInfo.major < 3:  # 适配python2
        apkFilePath = raw_input("apk文件全路径:".decode('utf-8').encode('gbk'))
    else:
        apkFilePath = input(u"apk文件全路径:")
else:
    apkFilePath = sys.argv[1]
cmd = "aapt dump badging " + apkFilePath + " | head -n 1"
print("cmd: " + cmd)
os.system(cmd)
os.system("pause")
