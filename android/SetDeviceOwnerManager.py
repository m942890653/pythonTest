# -*- coding: utf-8 -*-
# @author: zhoufeifei
# @date:   2021 0414

import shlex
import subprocess
import sys
import tempfile

DEBUG = False
DEFAULT_PKG_LIST = ["com.example.zheng.myapplication"]
DEFAULT_RECEIVER = "com.example.zheng.myapplication.receiver.MyDeviceAdminReceiver"


def logI(tag, msg):
    print("\n" + tag + "\n", msg)


def logD(tag, msg):
    if DEBUG:
        print("\n" + tag + "\n", msg)


def doCmd(cmd):
    stdoutFile = None
    stderrFile = None
    outResults = ''
    errResults = ''
    logD("doCmd", cmd)
    try:
        cmds = shlex.split(cmd)
        stdoutFile = tempfile.TemporaryFile(mode='w+')
        stderrFile = tempfile.TemporaryFile(mode='w+')
        p = subprocess.Popen(cmds, shell=False, stdout=stdoutFile.fileno(),
                             stderr=stderrFile.fileno())
        p.wait()
        stdoutFile.seek(0)
        outResults = stdoutFile.read()
        stderrFile.seek(0)
        errResults = stderrFile.read()
    except Exception as e:
        print(e)
    finally:
        if stdoutFile is not None:
            stdoutFile.close()
        if stderrFile is not None:
            stderrFile.close()
    return outResults + errResults


def doCmdAdbShell(cmd, device=""):
    if isEmpty(device):
        cmdResult = doCmd("adb shell " + cmd)
    else:
        cmdResult = doCmd("adb  -s {device}  shell " + cmd.format(device=device))
    logD("doCmdAdbShell:", cmdResult)
    return cmdResult


def getDevices():
    cmdResult = doCmd("adb devices")
    resultDevices = []
    lines = cmdResult.split("\n")
    for line in lines:
        if not line.endswith("device"):
            continue
        device = line.replace('device', '').strip()
        resultDevices.append(device)
    logI("getDevices: resultDevices ", resultDevices)
    return resultDevices


def isEmpty(obj):
    return obj is None or len(obj) <= 0


def getAllApp(cmdDevice=""):
    tag = "getAllApp:"
    cmdResult = doCmdAdbShell("pm list package", cmdDevice).replace("package:", '')
    logD(tag, cmdResult)
    appList = cmdResult.split("\n")
    logD(tag, appList)
    return appList


def resetDevice(cmdDevice=""):
    tag = "resetDevice:"
    cmdResult = doCmdAdbShell("pm list package -d", cmdDevice).replace(' ', '').replace("package:",
                                                                                        '').strip()
    if isEmpty(cmdResult):
        return []
    disableApp = cmdResult.split("\n")
    logD(tag, disableApp)
    for app in disableApp:
        try:
            cmdResult = doCmdAdbShell("pm enable " + app, cmdDevice)
            logD("resetDevice: cmdResult ", cmdResult)
        except Exception as e:
            print(e)

    cmdResult = doCmdAdbShell("pm list package -d", cmdDevice).replace("package:", '').replace(' ',
                                                                                               '').strip()
    logI(tag, disableApp)
    return cmdResult.split("\n")


class BaseManager:

    def __init__(self, cmdDevice=""):
        self.cmdDevice = cmdDevice


# 多用户（分身）管理
class UserManager(BaseManager):

    def getUsers(self):
        cmdResult = doCmdAdbShell("dumpsys user", self.cmdDevice)
        userList = []
        lines = cmdResult.split("\n")
        for line in lines:
            line = line.strip().replace(' ', '')
            if not line.startswith("UserInfo{"):
                continue

            line = line[len('UserInfo{'):]
            pos = line.find(':')
            assert 0 < pos
            userList.append(line[:pos])
        logI("getUsers:  userList  ", userList)
        return userList

    def deleteUser(self):
        devices = self.getUsers()
        for device in devices:
            if cmp(0, device):
                continue
            doCmdAdbShell("pm remove-user " + device, self.cmdDevice)


# 账户管理
class AccountManager(BaseManager):
    TAG_ACCOUNT = "AccountManager"

    def __init__(self, cmdDevice="", ignorePkg=""):
        BaseManager.__init__(self, cmdDevice)
        self.ignorePkg = ignorePkg

    @staticmethod
    def __parse_pkg__name__(line, prekey, enKey):
        pos = line.find(prekey)
        if pos < 0:
            return None
        line = line[pos + len(prekey):]
        pos = line.find('}')
        if pos < 0:
            return None
        pos1 = line.find(enKey)
        if 0 < pos1 < pos:
            pos = pos1
        return line[:pos]

    def getAccountPkg(self):
        result = doCmdAdbShell("dumpsys account", self.cmdDevice)
        lines = result.split('\n')
        accountPkg = []
        for line in lines:
            pkgName = ""
            line = line.strip().replace(' ', '')
            # Account {name= XXXXXXXXX, type=com.huawei.hwid}
            # ServiceInfo: AuthenticatorDescription {type=com.android.email}, ComponentInfo{com.android.email/com.kingsoft.email.service.LegacyImapAuthenticatorService}, uid 10059
            if line.startswith('Account{'):
                pkgName = self.__parse_pkg__name__(line, 'type=', ',')
            elif line.startswith('ServiceInfo:'):
                pkgName = self.__parse_pkg__name__(line, 'ComponentInfo{', '/')
            if isEmpty(pkgName) and pkgName not in accountPkg:
                continue
            if pkgName in self.ignorePkg:
                continue
            accountPkg.append(pkgName)

        logD(self.TAG_ACCOUNT + " getAccount:", accountPkg)
        return accountPkg

    # 修复账户
    def fixAccount(self):
        accountPkg = self.getAccountPkg()
        for pkgName in accountPkg:
            logD(self.TAG_ACCOUNT + "fixAccount: ", pkgName)
            if pkgName == self.ignorePkg:
                continue
            doCmdAdbShell("pm disable-user " + pkgName, self.cmdDevice)
        logI(self.TAG_ACCOUNT + "  disable app ", accountPkg)


# 设置强管管理
class DeviceOwnerManger(BaseManager):
    TAG = "DeviceOwnerManger"

    def __init__(self, pkgName, receiverName=None, cmdDevice="", ):
        BaseManager.__init__(self, cmdDevice)
        self.pkgName = pkgName
        if isEmpty(receiverName):
            self.receiverName = DEFAULT_RECEIVER
        else:
            self.receiverName = receiverName
        self.accountManager = AccountManager()

    def setDeviceOwner(self):
        cmdOwner = "dpm set-device-owner {pkg}/{receiver} --user 0".format(
            pkg=self.pkgName, receiver=self.receiverName)
        cmdResult = doCmdAdbShell(cmdOwner, self.cmdDevice)
        if 0 < cmdResult.find('Unexpected @ProvisioningPreCondition 99'):
            return self.setProfileOwner()
        return cmdResult

    def setProfileOwner(self):
        cmdProfile = "dpm  set-profile-owner {pkg}/{receiver} --user 0".format(
            pkg=self.pkgName, receiver=self.receiverName)
        return doCmdAdbShell(cmdProfile, self.cmdDevice)

    def isTargetApoDeviceOwner(self):
        dumpPolicy = doCmdAdbShell('dumpsys device_policy ' + self.pkgName).strip()
        if 0 < dumpPolicy.find("Device Owner") or 0 < dumpPolicy.find("Profile Owner"):
            return 0 < dumpPolicy.find(self.pkgName) and 0 < dumpPolicy.find(self.receiverName)
        return False

    def isDeviceOwner(self):
        dumpPolicy = doCmdAdbShell('dumpsys device_policy ' + self.pkgName).strip()
        return 0 < dumpPolicy.find("Device Owner") or 0 < dumpPolicy.find("Profile Owner")

    def getDeviceOwnerApp(self):
        if self.isDeviceOwner():
            lines = doCmdAdbShell('dumpsys device_policy ' + self.pkgName).split("\n")
            result = u"\n已经设置强管（owner is already set)"
            for line in lines:
                result += ("\n" + line)
                if 0 < line.find("admin="):
                    return result

        return "not find device owner app "


# ----------------------- test ------------------------------

def run(pkgName="", receiverName="", cmdDevice=""):
    TAG_RUN = "run"
    logI(TAG_RUN,
         "pkgName: " + pkgName + "\nreceiverName:  " + receiverName + "\ncmdDevice: " + cmdDevice)

    installApps = getAllApp()
    if isEmpty(pkgName):
        for pkg in DEFAULT_PKG_LIST:
            if pkg in installApps:
                pkgName = pkg
    else:
        if pkgName not in installApps:
            pkgName = ""
    if isEmpty(pkgName):
        logI(TAG_RUN, u"当前没有安装设置强管应用请安装,如果已经安装启动一下应用")
        exit("no install set app")

    deviceOwnerManger = DeviceOwnerManger(pkgName, receiverName)
    if deviceOwnerManger.isDeviceOwner():
        if deviceOwnerManger.isTargetApoDeviceOwner():
            exit("device owner success  ")
        else:
            exit(deviceOwnerManger.getDeviceOwnerApp())

    userManager = UserManager(cmdDevice)
    if 1 < len(userManager.getUsers()):
        logI(TAG_RUN, u"存在多用户请删除:(more user)\n\n自动删除: 1  (!!!自动删除用户(分身)信息将无法恢复，谨慎操作)")
        inputStr = raw_input("input:\n ")
        if cmp(1, inputStr):
            userManager.deleteUser()
        else:
            logI(TAG_RUN, u"手动删除多用户(设备分身)后重新执行脚本(again)")
            exit("delete user again .........")

    accountManager = AccountManager(cmdDevice, pkgName)
    if 0 < len(accountManager.getAccountPkg()):
        accountManager.fixAccount()

    accountPkg = accountManager.getAccountPkg()
    if 0 < len(accountPkg):
        for pkg in accountPkg:
            if pkgName == pkg:
                logI(TAG_RUN, u"设置强管的应用有账户需要手动删除")
                exit("account in set app " + pkg)

    deviceOwnerManger = DeviceOwnerManger(pkgName, receiverName, cmdDevice)
    try:
        if not deviceOwnerManger.isTargetApoDeviceOwner():
            logI(TAG_RUN, deviceOwnerManger.setDeviceOwner())

    finally:
        resetDevice()
        if deviceOwnerManger.isTargetApoDeviceOwner():
            logI(TAG_RUN, "device owner success")
        else:
            logI(TAG_RUN, "device owner fail")


if __name__ == '__main__':
    TAG_MAIN = "main"
    if len(getDevices()) <= 0:
        logI(TAG_MAIN, u"当前没有链接设备请检查")
        exit("no devices")

    arg = sys.argv[1:]
    if len(arg) == 2:
        run(arg[0], arg[1])
    elif 1 == len(arg):
        run(arg[0], arg[1])
    else:
        run()
