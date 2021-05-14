"""
斗地主记牌器
"""
import winguiauto
import win32gui
from PIL import ImageGrab, Image
import cv2 as cv


gameName = "欢乐斗地主"


def grabimg():
    # 获取程序窗口截图
    hwnd = winguiauto.findTopWindow(gameName)
    rect = win32gui.GetWindowPlacement(hwnd)[-1]
    image = ImageGrab.grab(rect)
    image.save("test.png")
