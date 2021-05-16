"""
斗地主记牌器
"""
import winguiauto
import win32gui
from PIL import ImageGrab, Image
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


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
    masked_img = mask_*img
    return masked_img


def match(queryImage, trainingImage):
    sift = cv.SIFT_create()  # 创建sift检测器
    kp1, des1 = sift.detectAndCompute(queryImage, None)
    kp2, des2 = sift.detectAndCompute(trainingImage, None)
    # 设置Flannde参数
    FLANN_INDEX_KDTREE = 0
    indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    searchParams = dict(checks=50)
    flann = cv.FlannBasedMatcher(indexParams, searchParams)
    matches = flann.knnMatch(des1, des2, k=2)
    # 设置好初始匹配值
    matchesMask = [[0, 0] for i in range(len(matches))]
    simi = 0
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.3 * n.distance:  # 舍弃小于0.7的匹配结果
            matchesMask[i] = [1, 0]
            simi += 1
    if simi > 5:
        print("True", simi)

    drawParams = dict(matchColor=(0, 0, 255), singlePointColor=(255, 0, 0), matchesMask=matchesMask,
                      flags=0)  # 给特征点和匹配的线定义颜色
    resultimage = cv.drawMatchesKnn(queryImage, kp1, trainingImage, kp2, matches, None, **drawParams)  # 画出匹配的结果
    plt.imshow(resultimage)
    plt.show()


def match_2(template, target):
    """
    由于模板匹配对于旋转和缩放的匹配效果不好，尝试通过插值对图像进行缩放，并没有改进匹配效果
    尝试对模板图像裁剪的更精准，提高了匹配效果
    todo: 尝试二值分割提高匹配效果
    :param template:
    :param target:
    :return:
    """
    # 获得模板图片的高宽尺寸
    theight, twidth = template.shape[:2]
    # 执行模板匹配，采用的匹配方式cv2.TM_SQDIFF_NORMED
    result = cv.matchTemplate(target, template, cv.TM_SQDIFF_NORMED)
    # 归一化处理
    cv.normalize(result, result, 0, 1, cv.NORM_MINMAX, -1)
    # 寻找矩阵（一维数组当做向量，用Mat定义）中的最大值和最小值的匹配结果及其位置
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    print(min_val, max_val)
    # 匹配值转换为字符串
    # 对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法min_val越趋近于0匹配度越好，匹配位置取min_loc
    # 对于其他方法max_val越趋近于1匹配度越好，匹配位置取max_loc
    strmin_val = str(min_val)
    # 绘制矩形边框，将匹配区域标注出来
    # min_loc：矩形定点
    # (min_loc[0]+twidth,min_loc[1]+theight)：矩形的宽高
    # (0,0,225)：矩形的边框颜色；2：矩形边框宽度
    cv.rectangle(target, min_loc, (min_loc[0] + twidth, min_loc[1] + theight), (0, 0, 225), 2)
    # 显示结果,并将匹配值显示在标题栏上
    cv.imshow("MatchResult----MatchingValue=" + strmin_val, target)
    cv.waitKey()
    cv.destroyAllWindows()


if __name__ == '__main__':
    # 测试掩模
    # img = cv.imread("imgs/test1.png")
    # masked_img = mask(img, mode=0)
    # cv.imshow("OpenCV", masked_img)
    # cv.waitKey()
    # cv.destroyAllWindows()

    # 测试图像匹配
    queryImage = cv.imread("imgs/A_4.png")
    # queryImage = cv.cvtColor(queryImage, cv.COLOR_RGB2BGR)
    trainingImage = cv.imread("imgs/test1.png")
    # trainingImage = cv.cvtColor(trainingImage, cv.COLOR_RGB2BGR)
    trainingImage = mask(trainingImage, mode=1)

    # match(queryImage, trainingImage)

    match_2(queryImage, trainingImage)
