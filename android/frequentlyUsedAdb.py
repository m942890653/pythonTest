import os

import time

from utils.textTool import TextTool


class AdbCommand:
    PackageName = "com.uusafe.emm.android"

    @staticmethod
    def get_devices():
        cmd = "adb shell getprop ro.product.model"
        deviceName = os.popen(cmd, 'r').read()
        if len(str(deviceName)) < 1:
            TextTool.printRed('没有连接设备，请检查！')
            return 0
        else:
            print("手机型号: " + deviceName)
            print("---" * 20)
            return 1

    def screenshot(self):
        name = "screenshot-" + str(int(time.time())) + ".png"
        os.system("adb shell screencap /mnt/sdcard/" + name)
        print("截图已保存在SD卡根目录下，文件名：" + name)

    @staticmethod
    def kill_app(package_name=None):
        print('kill...' + package_name)
        os.system("adb shell am force-stop " + package_name)

    @staticmethod
    def clean_app(package_name=None):
        print("clean..." + package_name)
        os.system("adb shell pm clear " + package_name)

    @staticmethod
    def uninstall_app(package_name=None):
        print("uninstall..." + package_name)
        os.system("adb uninstall " + package_name)

    @staticmethod
    def set_device_owner():
        print("---" * 10)
        cmd = 'adb shell dpm set-device-owner com.uusafe.emm.android/com.uusafe.sandbox.deviceowner.receiver.DeviceOwnerReceiver'
        content = os.popen(cmd, 'r').read()
        if "Success: Device owner set" in content:
            print("DeviceOwner(强管控) 开启成功^_^")

        elif "but device owner is already set" in content:
            print("DeviceOwner(强管控)之前已经开启.")

        elif "java.lang.SecurityException: Neither user 2000 nor current process has" in content:
            print("没有权限开启，以下是失败原因:")
            print(content)

        elif "Not allowed to set the device owner because there are already some accounts on the device" in content:
            print("开启失败，请删除设备上的第三方账户后重试")
        else:
            print("可能开启失败，请确保设备是5.0以上版本，并且没有第三方账户。返回内容如下：")
            print(content)

    print("__name__: " + __name__)
    if __name__ == '__main__':
        print("模块被直接运行")
