import win32gui
import pyautogui
import subprocess
import time

hwnd_active = win32gui.GetForegroundWindow()

subprocess.Popen(r'D:\software\OnTopReplica\OnTopReplica.exe')
time.sleep(0.5)
win32gui.SetForegroundWindow(hwnd_active)
pyautogui.hotkey('ctrl', 'shift', 'c')
