"""记牌器GUI"""
import PySide2
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QObject
from match import *
from threading import Thread


class Mysignal(QObject):
    """
    避免在多线程中更新QT
    """
    pass


class Stats(QMainWindow):

    def __init__(self):
        # 从文件中加载UI定义
        super(QMainWindow).__init__()
        self.FLAG = None
        self.ui = QUiLoader().load('doudizhu.ui')
        self.ui.button_start.clicked.connect(self.start)
        self.ui.button_end.clicked.connect(self.end)

    def update_table(self, rest_card):
        self.ui.table_record.item(0, 0).setText(str(rest_card.count("JOK1")))
        self.ui.table_record.item(0, 1).setText(str(rest_card.count("JOK2")))
        self.ui.table_record.item(0, 2).setText(str(rest_card.count("2")))
        self.ui.table_record.item(0, 3).setText(str(rest_card.count("A")))
        self.ui.table_record.item(0, 4).setText(str(rest_card.count("K")))
        self.ui.table_record.item(0, 5).setText(str(rest_card.count("Q")))
        self.ui.table_record.item(0, 6).setText(str(rest_card.count("J")))
        self.ui.table_record.item(0, 7).setText(str(rest_card.count("10")))
        self.ui.table_record.item(0, 8).setText(str(rest_card.count("9")))
        self.ui.table_record.item(0, 9).setText(str(rest_card.count("8")))
        self.ui.table_record.item(0, 10).setText(str(rest_card.count("7")))
        self.ui.table_record.item(0, 11).setText(str(rest_card.count("6")))
        self.ui.table_record.item(0, 12).setText(str(rest_card.count("5")))
        self.ui.table_record.item(0, 13).setText(str(rest_card.count("4")))
        self.ui.table_record.item(0, 14).setText(str(rest_card.count("3")))

    def start(self):
        self.FLAG = True
        ALL_card = []
        for file in os.listdir("imgs/template/"):
            ALL_card.append(file.split(".")[0])
        # app_img = cv.imread("imgs/test.png")
        app_img = grabimg()
        # cv.imshow("MatchResult----MatchingValue=", app_img)
        # cv.waitKey()
        # cv.destroyAllWindows()
        ALL_card = detect(ALL_card, app_img, mode=0)
        card_num = []
        for i in range(len(ALL_card)):
            card_num.append(ALL_card[i].split('_')[0])
        # 更新表格内容
        self.update_table(card_num)

        # 在新的线程里面不断的截图=》匹配剩余的图片=》更新
        def run_func(ALL_card):
            while self.FLAG:
                app_img = grabimg()
                ALL_card = detect(ALL_card, app_img, mode=1)
                card_num = []
                for i in range(len(ALL_card)):
                    card_num.append(ALL_card[i].split('_')[0])
                # 更新表格内容
                self.update_table(card_num)

        thread = Thread(target=run_func, args=(ALL_card, ))     # run_func结束之后，线程自动销毁
        thread.start()

    def end(self):
        self.FLAG = False
        self.ui.table_record.item(0, 0).setText("1")
        self.ui.table_record.item(0, 1).setText("1")
        for i in range(12):
            self.ui.table_record.item(0, i + 2).setText("4")


app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()
