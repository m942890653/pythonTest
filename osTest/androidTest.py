import ctypes
import os
import re

import sys

import shutil

import time

PackageName = "com.uusafe.emm.android"
PackageName2 = "com.uusafe.emm.android.helper"


def get_devices():
    cmd = "adb shell getprop ro.product.model"
    deviceName = os.popen(cmd, 'r').read()
    if len(str(deviceName)) < 1:
        printRed('没有连接设备，请检查！')
    else:
        print("手机型号: " + deviceName)
        print("---" * 20)

        # string_1 = "非法卸载的步骤：需要先清除数据[4] -> 手动取消设备管理器 -> 卸载[5]，注：强管控不要使用！"
        # print string_1.decode('utf-8')

        choice_method()


def choice_method():
    running = True
    while running:
        print('[1] install apk')
        print('[2] screenshot')
        print('[3] kill uu')
        print('[4] clean uu (be careful !!)')
        print('[5] uninstall uu')
        print('[6] DeviceOwner')
        print('[7] SD_card_log')
        print()
        s = input('please enter a number: ')

        if ".apk" in s:
            print('install...')
            install_ENCN(s)
        elif int(s) == 1:
            print("install")
            install()
            running = False
        elif int(s) == 2:
            print("screenshot")
            screenshot()
            running = False
        elif int(s) == 3:
            print("kill_uu")
            kill_uu()
        elif int(s) == 4:
            print("clean_uu")
            clean_uu()
            running = False
        elif int(s) == 5:
            print("uninstall_uu")
            uninstall_uu()
        elif int(s) == 6:
            print('DeviceOwner')
            setDeviceOwner()
            running = False
        elif int(s) == 7:
            print("logcat")
            # logcat()
            running = False
        else:
            print('input Erroe! EXIT!')
            running = False


def install_ENCN(apk):
    path1 = os.getcwd()
    # 以下判断字符串是否包含简体中文
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    match = zhPattern.search(apk)

    if match:  # 包含中文
        if os.path.exists('tempDel'):
            shutil.rmtree('tempDel')
        else:
            os.mkdir('tempDel')
        shutil.copy(apk, path1 + '//tempDel//')
        apk = os.path.split(apk)[1]  # 去掉路径，取文件名
        newName = path1 + '//tempDel//' + apk
        os.rename(newName, path1 + '//tempDel//' + "001.apk")
        name2 = path1 + '//tempDel//' + "001.apk"

        cmd = 'adb install -r ' + name2
        content = os.popen(cmd, 'r').read()
        if 'Success' in content:
            print('install Success.')
        elif '_FAILED_' in content:
            print(content)
        else:
            print('other Error !!!')
            print(content)
        print('----------------------------------')
        shutil.rmtree('tempDel')
    else:  # 字符串不包含中文时
        cmd = 'adb install -r ' + apk
        content = os.popen(cmd, 'r').read()

        # 华为畅享7安装成功后 content 为空，魅蓝2正常
        if "Success" in content:
            print('install Success.')
        elif '_FAILED_' in content:
            print(content)
        else:
            print('other Error !!!')
            print(content)
        print('----------------------------------')


def install():
    running = True
    while running:
        string_1 = "拖动apk到这里，按Enter键安装，文件名不能有空格"
        print(string_1)
        s = input('')
        print('install...')
        if ".apk" in str(s):
            apk = str(s)
            install_ENCN(apk)
        else:
            print('input Erroe! EXIT!')
            running = False


def screenshot():
    name = "screenshot-" + str(int(time.time())) + ".png"
    os.system("adb shell screencap /mnt/sdcard/" + name)
    print("截图已保存在SD卡根目录下，文件名：" + name)


def kill_uu():
    print('kill...')
    os.system("adb shell am force-stop " + PackageName)


def clean_uu():
    print("clean_uu...")
    os.system("adb shell pm clear " + PackageName)


def uninstall_uu():
    print('uninstall...')
    print()
    cmd = "adb uninstall " + PackageName
    content = os.popen(cmd, 'r').read()
    cmd2 = "adb uninstall " + PackageName2
    content2 = os.popen(cmd2, 'r').read()
    print(content)
    print(content2)


def setDeviceOwner():
    print("---" * 10)
    cmd = 'adb shell dpm set-device-owner com.uusafe.emm.android/com.uusafe.sandbox.deviceowner.receiver.DeviceOwnerReceiver'
    content = os.popen(cmd, 'r').read()
    if "Success: Device owner set to package com.uusafe.emm.android" in content:
        print("DeviceOwner(强管控) 开启成功① ^_^")
    elif "Success: Device owner set to package ComponentInfo{com.uusafe.emm.android/com.uusafe.sandbox.deviceowner.receiver}" in content:
        print("DeviceOwner(强管控) 开启成功② ^_^")

    elif "but device owner is already set" in content:
        print("DeviceOwner(强管控)之前已经开启.")

    elif "java.lang.SecurityException: Neither user 2000 nor current process has" in content:
        print("没有权限开启，实在想开，可以恢复出厂试试。以下是失败原因，供参考")
        print(content)

    elif "Not allowed to set the device owner because there are already some accounts on the device" in content:
        print("开启失败，请删除设备上的第三方账户后重试")
    else:
        print("可能开启失败，请确保设备是5.0以上版本，并且没有第三方账户。返回内容如下：")
        print(content)


##################################################################

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

# Windows CMD命令行 字体颜色定义 text colors
FOREGROUND_BLUE = 0x09  # blue.
FOREGROUND_GREEN = 0x0a  # green.
FOREGROUND_RED = 0x0c  # red.

std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool


# reset white
def resetColor():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)


# 绿色
def printGreen(mess):
    set_cmd_text_color(FOREGROUND_GREEN)
    sys.stdout.write(mess)
    resetColor()


# 红色
def printRed(mess):
    set_cmd_text_color(FOREGROUND_RED)
    sys.stdout.write(mess)
    resetColor()


##################################################################

get_devices()
