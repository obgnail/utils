import subprocess
import time

import win32api
import win32con
import win32gui


class Skipper:
    def __init__(self, totalcmd_path):
        self.totalcmd_path = totalcmd_path
        self.class_name = 'TNASTYNAGSCREEN'
        self.sleep_time = 1
        self.target_control_idx = 3
        self.control_idx = 0
        self.value = ""

    def find_num(self, hwnd, param):
        if self.control_idx == self.target_control_idx:
            self.value = win32gui.GetWindowText(hwnd)
        self.control_idx += 1

    def run(self):
        subprocess.Popen(self.totalcmd_path)
        time.sleep(self.sleep_time)
        handle = win32gui.FindWindow(self.class_name, None)
        win32gui.EnumChildWindows(handle, self.find_num, None)
        key = {
            "1": win32con.VK_NUMPAD1,
            "2": win32con.VK_NUMPAD2,
            "3": win32con.VK_NUMPAD3,
        }[self.value]
        win32api.PostMessage(handle, win32con.WM_KEYDOWN, key, 0)


if __name__ == '__main__':
    totalcmd_path = r'd:\software\totalcmd\TOTALCMD64.EXE'
    Skipper(totalcmd_path).run()
