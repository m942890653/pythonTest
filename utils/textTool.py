import ctypes
import sys


class TextTool:
    # Windows CMD命令行 字体颜色定义 text colors
    FOREGROUND_BLUE = 0x09  # blue.
    FOREGROUND_GREEN = 0x0a  # green.
    FOREGROUND_RED = 0x0c  # red.
    STD_OUTPUT_HANDLE = -11
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    @staticmethod
    def set_cmd_text_color(color, handle=std_out_handle):
        Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return Bool

    @staticmethod
    # 红色
    def printRed(msg):
        TextTool.set_cmd_text_color(TextTool.FOREGROUND_RED)
        sys.stdout.write(msg)
        TextTool.resetColor()

    @staticmethod
    def resetColor():
        TextTool.set_cmd_text_color(
            TextTool.FOREGROUND_RED | TextTool.FOREGROUND_GREEN | TextTool.FOREGROUND_BLUE)
