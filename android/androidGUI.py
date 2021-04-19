# coding=utf-8
from tkinter import *

# 不加这行在命令行直接运行不成功
sys.path.append(r"C:\Users\zheng\Desktop\pythonTest")
from android.frequentlyUsedAdb import AdbCommand

PackageName = "com.uusafe.emm.android"
adbCommand = AdbCommand()

count = AdbCommand.get_devices()
if count == 0:
    quit()


def callback():
    print("点了")


def callback2():
    print("点了截屏")
    adbCommand.screenshot()


def callback3():
    print("点了杀应用")
    AdbCommand.kill_app(package_name=PackageName)


def callback4():
    print("点了清除应用数据")
    AdbCommand.clean_app(package_name=PackageName)


def callback5():
    print("点了开启DeviceOwner")
    AdbCommand.set_device_owner()


def callback6():
    print("点了卸载应用")
    AdbCommand.uninstall_app(package_name=PackageName)


root = Tk()

frame1 = Frame(root)
# 加一个按钮
theButton = Button(frame1, text="install apk", command=callback)
theButton.pack()

screenshotButton = Button(frame1, text="屏幕截图", command=callback2)
screenshotButton.pack()

forceStopBtn = Button(frame1, text="force stop EMM", command=callback3)
forceStopBtn.pack()

clearBtn = Button(frame1, text="清除应用数据", command=callback4)
clearBtn.pack()

setDeviceOwnerBtn = Button(frame1, text="开启DeviceOwner", command=callback5)
setDeviceOwnerBtn.pack()

uninstallBtn = Button(frame1, text="卸载EMM", command=callback6)
uninstallBtn.pack()

frame1.pack(padx=10, pady=10)

mainloop()
