"""
匹配方法
"""
from matplotlib import pyplot as plt
import pyautogui
import os
from utils import *


def match_1(queryImage, trainingImage):
    """
    SIFT特征匹配
    模板图像特征太简单 匹配效果很差
    """
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
        if m.distance < 0.7 * n.distance:
            matchesMask[i] = [1, 0]
            simi += 1
    if simi > 5:
        print("True", simi)

    drawParams = dict(matchColor=(0, 0, 255), singlePointColor=(255, 0, 0), matchesMask=matchesMask,
                      flags=0)
    resultimage = cv.drawMatchesKnn(queryImage, kp1, trainingImage, kp2, matches, None, **drawParams)  # 画出匹配的结果
    plt.imshow(resultimage)
    plt.show()


def match_2(template, target):
    """
    模板匹配
     - 由于模板匹配对于旋转和缩放的匹配效果不好，尝试通过插值对图像进行缩放，并没有改进匹配效果
     - 尝试对模板图像裁剪的更精准，提高了匹配效果
    """
    # 执行模板匹配，采用的匹配方式cv2.TM_SQDIFF_NORMED
    result = cv.matchTemplate(target, template, cv.TM_SQDIFF_NORMED)
    cv.normalize(result, result, 0, 1, cv.NORM_MINMAX, -1)
    # 寻找矩阵（一维数组当做向量，用Mat定义）中的最大值和最小值的匹配结果及其位置
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    print(min_val, max_val)
    # 匹配值转换为字符串
    # 对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法min_val越趋近于0匹配度越好，匹配位置取min_loc
    # 对于其他方法max_val越趋近于1匹配度越好，匹配位置取max_loc
    strmin_val = str(min_val)
    # 绘制矩形边框，将匹配区域标注出来
    # 获得模板图片的高宽尺寸
    theight, twidth = template.shape[:2]
    cv.rectangle(target, min_loc, (min_loc[0] + twidth, min_loc[1] + theight), (0, 0, 225), 2)
    cv.imshow("MatchResult" + strmin_val, target)
    cv.waitKey()
    cv.destroyAllWindows()


def match_3(haystackImage, mode=0):
    """
     - 可以统一管理置信区间
    :param haystackImage:
    :return:
    """
    card = []
    if mode:
        file_ = "imgs/template_2/"
    else:
        file_ = "imgs/template/"
    for file in os.listdir("imgs/template/"):
        result = pyautogui.locateAll(needleImage=file_ + file, haystackImage=haystackImage, confidence=0.96)
        result = list(result)
        if len(result) != 0:
            card.append(file.split(".")[0])
    # print(card)
    return card
    # result = result[-1]
    # cv.rectangle(trainingImage, (result[0], result[1]), (result[0] + result[2], result[1] + result[3]), (0, 0, 225), 2)
    # cv.imshow("MatchResult----MatchingValue=", trainingImage)
    # cv.waitKey()
    # cv.destroyAllWindows()


def detect(ALL_card, img, mode=1):
    """
    :param ALL_card:
    :param img:
    :param mode:
    :return: 剩余的卡
    """
    img_mask = mask(img, mode=mode)
    # cv.imshow("masked image", img_mask)
    # cv.waitKey()
    # cv.destroyAllWindows()
    card = match_3(img_mask, mode=mode)
    while card:
        if card[-1] in ALL_card:
            ALL_card.remove(card[-1])
        card.pop()
    return ALL_card


if __name__ == '__main__':
    trainingImage = cv.imread("imgs/test.png")
    trainingImage = mask(trainingImage, mode=0)

    # match_1(queryImage, trainingImage)
    # match_2(queryImage, trainingImage)
    card = match_3(trainingImage, mode=0)
