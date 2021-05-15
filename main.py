"""
斗地主记牌器
"""
import winguiauto
import win32gui
from PIL import ImageGrab, Image
import cv2 as cv
import numpy as np


gameName = "欢乐斗地主"


def grabimg():
    # 获取程序窗口截图
    hwnd = winguiauto.findTopWindow(gameName)
    rect = win32gui.GetWindowPlacement(hwnd)[-1]
    image = ImageGrab.grab(rect)
    image.save("imgs/test1.png")
    return cv.cvtColor(np.asarray(image), cv.COLOR_RGB2BGR)     # PIL图像编码转cv图像编码


def mask(img, mode=1):
    if mode:
        # 取别人的牌
        mask_loc = "imgs/mask1.png"
    else:
        # 取自己的牌
        mask_loc = "imgs/mask0.png"
    mask_ = cv.imread(mask_loc)
    print(np.shape(mask_))
    masked_img = mask_*img
    return masked_img


# todo: 测试图像匹配
if __name__ == '__main__':
    img = cv.imread("imgs/test1.png")
    masked_img = mask(img, mode=1)
    cv.imshow("OpenCV", masked_img)
    cv.waitKey()
    cv.destroyAllWindows()

