
import cv2 as cv
import winguiauto
import win32gui
from PIL import ImageGrab, Image
import numpy as np


def grabimg():
    # 获取程序窗口截图
    game_name = "欢乐斗地主"
    hwnd = winguiauto.findTopWindow(game_name)
    rect = win32gui.GetWindowPlacement(hwnd)[-1]
    image = ImageGrab.grab(rect)
    # image.save("imgs/test1.png")
    return cv.cvtColor(np.asarray(image), cv.COLOR_RGB2BGR)     # PIL图像编码转cv图像编码


def mask(img, mode=0):
    """
    todo: 对于一次性出很多牌，可能会用两行来显示，下面的牌会遮挡住上面一行的花色
    :param mode: 选择裁剪的对象
        0: 自己手牌
        1: 别人的牌
    :return: top, left, height, width
    """
    if mode:
        top = 190
        left = 150
        height = 76
        width = 744
    else:
        top = 410
        left = 13
        height = 92
        width = 933
    img_crop = img[top:top + height, left:left + width]
    return img_crop


def fix_resolution():
    """
    对小程序窗口进行缩放时，长宽比例是固定的，
    因此只需要按照对应的比例缩放窗口截图就可以解决分辨率的问题
    :return:
    """
    pass


if __name__ == '__main__':
    grabimg()
