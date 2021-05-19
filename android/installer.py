# @author: zheng
# @date:   2021/4/27 10:12
import os
import sys
source = sys.argv[1]
cmd = "adb install -r -t " + source
print("cmd: " + cmd)
os.system(cmd)
os.system("pause")