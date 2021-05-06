# 文件名称：EnglishHub_ui.py
# 主要功能：程序主界面
# 最后修改时间: 2021/04/27 16:24
# ======================================================================

from PyQt5.Qt import *
from PyQt5.QtGui import QPixmap
from from__ import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets, QtCore
import sys

# from DataBase import *
# from FavoriteWords import *

from OnlineTranslation_ui import OnlineTranslationUI
from Dictionary_ui import DictionaryUI
from FavoriteWords_ui import FavoriteWordsUI
from WordsTest_ui import WordsForTestUI
from Login_ui import LoginUI
from Login_ui import RegisterUI


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('EnglishHub')  # 界面标题
        self.resize(1024, 720)  # 界面初始大小
        self.setMinimumSize(1024, 720)  # 固定界面最小大小
        self.setFixedSize(1024, 720)  # 界面大小不可变

        self.controlStrip = QVBoxLayout()  # 垂直布局的功能栏
        self.appName = QLabel('EnglishHub')  # 应用名称
        self.button1 = QPushButton('在线翻译')
        self.button2 = QPushButton('英汉词典')
        self.button3 = QPushButton('每日背单词')
        self.button4 = QPushButton('单词测试')
        self.button5 = QPushButton('单词收藏夹')
        self.button6 = QPushButton('每日新闻')

        self.controlStrip.addWidget(self.appName)
        self.controlStrip.addWidget(self.button1)
        self.controlStrip.addWidget(self.button2)
        self.controlStrip.addWidget(self.button3)
        self.controlStrip.addWidget(self.button4)
        self.controlStrip.addWidget(self.button5)
        self.controlStrip.addWidget(self.button6)
        self.controlStrip.setStretch(0, 1)
        self.controlStrip.setStretch(1, 1)
        self.controlStrip.setStretch(2, 1)
        self.controlStrip.setStretch(3, 1)
        self.controlStrip.setStretch(4, 1)
        self.controlStrip.setStretch(5, 1)
        self.controlStrip.setStretch(6, 1)

        self.loginUI = LoginUI()
        self.registerUI = RegisterUI()
        self.onlineTranslationUI = OnlineTranslationUI()

        self.stack1 = self.onlineTranslationUI  # 堆栈界面
        self.stack2 = DictionaryUI()
        self.stack3 = QWidget()
        self.stack4 = WordsForTestUI()
        self.stack5 = FavoriteWordsUI()
        self.stack6 = QWidget()

        self.stack = QStackedWidget()  # 堆栈控件，放置对应功能的界面
        self.stack.addWidget(self.stack1)  # 放入对应界面
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)
        self.stack.addWidget(self.stack4)
        self.stack.addWidget(self.stack5)
        self.stack.addWidget(self.stack6)

        self.userInfoLabel = QLabel('未登录')  # 用户名欢迎标题
        self.userButton = QPushButton('登录')  # 用户登录或注销的按钮
        hbox2 = QHBoxLayout()
        hbox2.addStretch()
        hbox2.addWidget(self.userInfoLabel)
        hbox2.addWidget(self.userButton)
        hbox2.setContentsMargins(30, 0, 30, 0)

        vbox2 = QVBoxLayout()  # 右侧功能界面
        vbox2.addLayout(hbox2)
        vbox2.addWidget(self.stack)

        hBox = QHBoxLayout()  # 主界面的水平控件
        hBox.addLayout(self.controlStrip)  # 主界面左侧为菜单
        hBox.addLayout(vbox2)  # 右侧为对应功能界面
        hBox.setStretch(0, 1)
        hBox.setStretch(1, 4)
        self.setLayout(hBox)

        self.FormatWidget()

        # 槽函数绑定
        self.button1.clicked.connect(self.OnClickButton1)
        self.button2.clicked.connect(self.OnClickButton2)
        self.button3.clicked.connect(self.OnClickButton3)
        self.button4.clicked.connect(self.OnClickButton4)
        self.button5.clicked.connect(self.OnClickButton5)
        self.button6.clicked.connect(self.OnClickButton6)
        self.userButton.clicked.connect(self.OnClickUserButton)
        self.loginUI.registerButton.clicked.connect(self.loginUI.Close)
        self.loginUI.registerButton.clicked.connect(self.registerUI.Open)
        self.registerUI.loginButton.clicked.connect(self.registerUI.Close)
        self.registerUI.loginButton.clicked.connect(self.loginUI.Open)

        self.user = ''

    def FormatWidget(self):
        """
        设置控件格式
        """
        pic = QPixmap('label.png')
        self.appName.setPixmap(pic)
        self.appName.setMaximumHeight(100)
        self.appName.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        sizePolicy = QSizePolicy()  # 设置按钮控件格式为水平垂直自动扩展
        sizePolicy.setVerticalPolicy(QSizePolicy.Expanding)
        sizePolicy.setHorizontalPolicy(QSizePolicy.Expanding)
        self.button1.setSizePolicy(sizePolicy)
        self.button2.setSizePolicy(sizePolicy)
        self.button3.setSizePolicy(sizePolicy)
        self.button4.setSizePolicy(sizePolicy)
        self.button5.setSizePolicy(sizePolicy)
        self.button6.setSizePolicy(sizePolicy)

        font = QFont()
        font.setFamily('微软雅黑')
        font.setPointSize(10)
        sizePolicy.setHorizontalPolicy(QSizePolicy.Fixed)
        sizePolicy.setVerticalPolicy(QSizePolicy.Fixed)
        self.userInfoLabel.setSizePolicy(sizePolicy)
        self.userInfoLabel.setFont(font)
        self.userButton.setSizePolicy(sizePolicy)
        self.userButton.setFont(font)

    def OnClickUserButton(self):
        """
        用户按钮槽函数
        :return:
        """
        if self.user == '':
            self.loginUI.signal.connect(self.SetUserName)
            self.loginUI.show()
        else:
            msgBox = QMessageBox().question(QWidget(), "询问", "确认退出登录？", QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.No)
            if msgBox == QMessageBox.Yes:
                self.user = ''
                self.userButton.setText('登录')
                self.userInfoLabel.setText('未登录')
                self.onlineTranslationUI.SetUsable(False)

    def SetUserName(self, data):
        """
        设置用户名
        :param data: 用户名字符串
        :return:
        """
        self.user = data
        self.userInfoLabel.setText('欢迎：' + data)
        self.userButton.setText('退出登录')
        self.loginUI.Close()
        self.onlineTranslationUI.SetUsable(True)

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

    def OnClickButton5(self):
        """
        按钮5槽函数
        :return:
        """
        if self.stack.currentIndex() != 4:
            self.stack.setCurrentIndex(4)
            self.stack5.Refresh()

    def OnClickButton6(self):
        """
        按钮6槽函数
        :return:
        """
        if self.stack.currentIndex() != 5:
            self.stack.setCurrentIndex(5)

    def closeEvent(self, event):
        """
        使用sys.exit(0)时只要关闭了主窗口，所有关联的子窗口也会全部关闭
        """
        sys.exit(0)


if __name__ == '__main__':
    # db = sqlite3.connect(dbFile)
    # dbc = db.cursor()
    # sql = "select word from dictionary where tag like ?"
    # dbc.execute(sql, ('%cet6%',))
    # execResult = dbc.fetchall()
    # reciteList = [i[0] for i in execResult][:20]
    # # print(reciteList)
    # f = Favorites()
    # for i in reciteList:
    #     f.Add(i)

    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


