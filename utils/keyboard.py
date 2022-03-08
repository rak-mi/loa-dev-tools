from pynput.keyboard import Key, Controller
import win32gui

keyboard = Controller()
hwnd = win32gui.FindWindowEx(0,0,0, "LOST ARK (64-bit, DX11) v.2.0.3.1")
win32gui.SetForegroundWindow(hwnd)

with keyboard.pressed(Key.alt):
    keyboard.press('y')
    keyboard.release('y') 