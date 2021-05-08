# 文件名称：EnglishHub.py
# 主要功能：程序主界面
# ======================================================================

import sys
import os
import qtawesome
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.Qt import *
from PyQt5 import QtWidgets, QtCore

from OnlineTranslation_ui import OnlineTranslationUI
from Dictionary_ui import DictionaryUI
from StudyEnglish_ui import StudyEnglishUI
from FavoriteWords_ui import FavoriteWordsUI
from Feedback_ui import FeedbackUI
from Introduction_ui import Ui_IntroductionUI


class StudyEnglish_UI(QWidget, StudyEnglishUI):
    def __init__(self):
        super(StudyEnglish_UI, self).__init__()
        self.setupUi(self)


class Introduction_UI(QWidget, Ui_IntroductionUI):
    def __init__(self):
        super(Introduction_UI, self).__init__()
        self.setupUi(self)


class OnlineTranslation_UI(QWidget, OnlineTranslationUI):
    def __init__(self):
        super(OnlineTranslation_UI, self).__init__()
        self.setupUi(self)


class Feedback_UI(QWidget, FeedbackUI):
    def __init__(self):
        super(Feedback_UI, self).__init__()
        self.setupUi(self)


class MainWindow(QMainWindow):
    """
    主界面窗口
    """
    user = ''  # 当前登录用户

    def __init__(self):
        super().__init__()
        if not os.path.exists("Data"):
            os.makedirs("Data")
        if not os.path.exists("log"):
            os.makedirs("log")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('EnglishHub')  # 界面标题
        self.setFixedSize(1200, 750)  # 界面大小不可变

        self.mainWidget = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QGridLayout()
        self.mainWidget.setLayout(self.mainLayout)

        self.leftWidget = QtWidgets.QWidget()  # 创建左侧部件
        self.leftWidget.setObjectName('left_widget')
        self.leftLayout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.leftWidget.setLayout(self.leftLayout)  # 设置左侧部件布局为网格

        self.rightFrame = QtWidgets.QFrame()  # 创建右侧部件
        self.rightFrame.setObjectName('right_frame')

        self.mainLayout.addWidget(self.leftWidget, 0, 0, 12, 3)  # 左侧部件在第0行第0列，占8行3列
        self.mainLayout.addWidget(self.rightFrame, 0, 3, 12, 9)  # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.mainWidget)  # 设置窗口主部件

        self.leftClose = QtWidgets.QPushButton("")  # 关闭按钮
        self.leftMini = QtWidgets.QPushButton("")  # 最小化按钮

        self.appName = QPushButton('EnglishHub')  # 应用名称
        self.appName.setObjectName('left_label')
        self.support = QPushButton('联系与帮助')
        self.support.setObjectName('left_label')
        self.button1 = QPushButton(qtawesome.icon('fa.globe', color='white'), '在线翻译')
        self.button2 = QPushButton(qtawesome.icon('fa.book', color='white'), '英汉词典')
        self.button3 = QPushButton(qtawesome.icon('fa.leanpub', color='white'), '每日背单词')
        self.button4 = QPushButton(qtawesome.icon('fa.bookmark', color='white'), '单词收藏夹')
        self.button5 = QPushButton(qtawesome.icon('fa.newspaper-o', color='white'), '每日新闻')
        self.button6 = QPushButton(qtawesome.icon('fa.comment', color='white'), "反馈建议")
        self.button7 = QPushButton(qtawesome.icon('fa.star', color='white'), "关于我们")
        self.button1.setObjectName('left_button')
        self.button2.setObjectName('left_button')
        self.button3.setObjectName('left_button')
        self.button4.setObjectName('left_button')
        self.button5.setObjectName('left_button')
        self.button6.setObjectName('left_button')
        self.button7.setObjectName('left_button')

        hbox = QHBoxLayout()
        self.userInfoLabel = QLabel('未登录')  # 用户名欢迎标题
        self.userButton = QPushButton('登录')  # 用户登录或注销的按钮
        hbox.addWidget(self.userInfoLabel)
        hbox.addWidget(self.userButton)

        self.FormatWidget()

        self.leftLayout.addWidget(self.leftMini, 0, 0, 1, 1)
        self.leftLayout.addWidget(self.leftClose, 0, 2, 1, 1)
        self.leftLayout.addWidget(self.appName, 0, 1, 1, 1)
        self.leftLayout.addLayout(hbox, 2, 0, 1, 3)
        self.leftLayout.addWidget(self.button1, 3, 0, 1, 3)
        self.leftLayout.addWidget(self.button2, 4, 0, 1, 3)
        self.leftLayout.addWidget(self.button3, 5, 0, 1, 3)
        self.leftLayout.addWidget(self.button4, 7, 0, 1, 3)
        self.leftLayout.addWidget(self.button5, 8, 0, 1, 3)
        self.leftLayout.addWidget(self.support, 9, 0, 1, 3)
        self.leftLayout.addWidget(self.button6, 10, 0, 1, 3)
        self.leftLayout.addWidget(self.button7, 11, 0, 1, 3)
        # self.leftLayout.addWidget(self.button1, 2, 0, 1, 3)
        # self.leftLayout.addWidget(self.button2, 3, 0, 1, 3)
        # self.leftLayout.addWidget(self.button3, 4, 0, 1, 3)
        # self.leftLayout.addWidget(self.button4, 6, 0, 1, 3)
        # self.leftLayout.addWidget(self.button5, 7, 0, 1, 3)
        # self.leftLayout.addWidget(self.support, 8, 0, 1, 3)
        # self.leftLayout.addWidget(self.button6, 9, 0, 1, 3)
        # self.leftLayout.addWidget(self.button7, 10, 0, 1, 3)

        self.stack1 = OnlineTranslation_UI()  # 堆栈界面
        self.stack2 = DictionaryUI()
        self.stack3 = StudyEnglish_UI()
        self.stack4 = FavoriteWordsUI()
        self.stack5 = QWidget()
        self.stack6 = Feedback_UI()
        self.stack7 = Introduction_UI()

        self.loginButton = QPushButton

        self.stack = QStackedLayout(self.rightFrame)  # 堆栈控件，放置对应功能的界面
        self.stack.addWidget(self.stack1)  # 放入对应界面
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)
        self.stack.addWidget(self.stack4)
        self.stack.addWidget(self.stack5)
        self.stack.addWidget(self.stack6)
        self.stack.addWidget(self.stack7)

        # 槽函数绑定
        self.button1.clicked.connect(self.OnClickButton1)
        self.button2.clicked.connect(self.OnClickButton2)
        self.button3.clicked.connect(self.OnClickButton3)
        self.button4.clicked.connect(self.OnClickButton4)
        self.button5.clicked.connect(self.OnClickButton5)
        self.button6.clicked.connect(self.OnClickButton6)
        self.button7.clicked.connect(self.OnClickButton7)

        self.leftClose.clicked.connect(self.close)
        self.leftMini.clicked.connect(self.showMinimized)
        self.leftClose.setFixedSize(40, 40)  # 设置关闭按钮的大小
        self.leftMini.setFixedSize(40, 40)  # 设置最小化按钮大小

        self.leftClose.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:10px;}QPushButton:hover{background:red;}''')
        self.leftMini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:10px;}QPushButton:hover{background:green;}''')

        self.leftWidget.setStyleSheet('''
                QPushButton{
                    border:none;
                    color:white;
                }
                QPushButton#left_label{
                    border:none;
                    border-bottom:1px solid white;
                    font-size:30px;
                    font-weight:700;
                    font-family: "微软雅黑", Helvetica, Arial, sans-serif;
                }
                QPushButton#left_button{
                    font-size:20px;
                }
                QPushButton#left_button:hover{
                    background-color:black;
                    border-left:4px solid red;
                    border-right:4px solid red;
                    border-top:4px solid red;
                    border-bottom:4px solid red;
                    border-radius:10px;
                    font-weight:1000;
                    color:white;
                }
                QWidget#left_widget{
                    background:gray;
                    border-top:1px solid white;
                    border-bottom:1px solid white;
                    border-left:1px solid white;
                    border-top-left-radius:10px;
                    border-bottom-left-radius:10px;
                }
        ''')

        self.rightFrame.setStyleSheet('''
            QFrame#right_frame{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "微软雅黑", Helvetica, Arial, sans-serif;
            }
        ''')

        self.setWindowOpacity(0.95)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.mainLayout.setSpacing(0)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mFlag = True
            self.mPosition = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.mFlag:
            self.move(QMouseEvent.globalPos() - self.mPosition)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.mFlag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def FormatWidget(self):
        """
        设置控件格式
        """
        sizePolicy = QSizePolicy()  # 设置按钮控件格式为水平垂直自动扩展
        sizePolicy.setVerticalPolicy(QSizePolicy.Expanding)
        sizePolicy.setHorizontalPolicy(QSizePolicy.Expanding)
        self.button1.setSizePolicy(sizePolicy)
        self.button2.setSizePolicy(sizePolicy)
        self.button3.setSizePolicy(sizePolicy)
        self.button4.setSizePolicy(sizePolicy)
        self.button5.setSizePolicy(sizePolicy)
        self.button6.setSizePolicy(sizePolicy)
        self.button7.setSizePolicy(sizePolicy)


    def OnClickButton1(self):
        """
        按钮1槽函数
        :return:
        """
        if self.stack.currentIndex() != 0:
            self.stack.setCurrentIndex(0)

    def OnClickButton2(self):
        """
        按钮2槽函数
        :return:
        """
        if self.stack.currentIndex() != 1:
            self.stack.setCurrentIndex(1)

    def OnClickButton3(self):
        """
        按钮3槽函数
        :return:
        """
        if self.stack.currentIndex() != 2:
            self.stack.setCurrentIndex(2)

    def OnClickButton4(self):
        """
        按钮4槽函数
        :return:
        """
        if self.stack.currentIndex() != 3:
            self.stack.setCurrentIndex(3)
            self.stack4.Refresh()

    def OnClickButton5(self):
        """
        按钮5槽函数
        :return:
        """
        if self.stack.currentIndex() != 4:
            self.stack.setCurrentIndex(4)

    def OnClickButton6(self):
        """
        按钮6槽函数
        :return:
        """
        if self.stack.currentIndex() != 5:
            self.stack.setCurrentIndex(5)

    def OnClickButton7(self):
        """
        按钮7槽函数
        :return:
        """
        if self.stack.currentIndex() != 6:
            self.stack.setCurrentIndex(6)

    def OnClickButton8(self):
        """
        按钮8槽函数
        :return:
        """
        if self.stack.currentIndex() != 7:
            self.stack.setCurrentIndex(7)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


