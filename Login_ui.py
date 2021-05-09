# 文件名称：Login_ui.py
# 主要功能：登录注册界面
# ======================================================================

from PyQt5 import QtCore
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import _thread

from Client import *


class MyBtn(QPushButton):
    def __init__(self, text):
        super().__init__(text)

    def enterEvent(self, a0):
        self.setStyleSheet("color:red; border:none")

    def leaveEvent(self, a0):
        self.setStyleSheet("color:black; border:none")


class LoginUI(QMainWindow, QThread):
    """
    用户登录界面类
    """
    signal = pyqtSignal(str)

    def __init__(self):
        super(LoginUI, self).__init__()
        self.setWindowTitle('登录')  # 界面标题
        self.setFixedSize(400, 400)  # 界面大小不可变

        self.label = QLabel('EnglishHub')  # 应用图标
        self.label.setObjectName('label')
        self.username = QLineEdit()  # 用户名输入框
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.username)
        hbox1.setContentsMargins(30, 0, 30, 0)

        self.password = QLineEdit()  # 密码输入框
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.password)
        hbox2.setContentsMargins(30, 0, 30, 0)

        self.warningLabel = QLabel('提示框')  # 登录提示
        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.warningLabel)
        hbox5.addStretch()
        hbox5.setContentsMargins(30, 0, 30, 0)

        self.loginButton = QPushButton('登录')
        self.cancelButton = QPushButton('取消')
        self.loginButton.setObjectName('main_button')
        self.cancelButton.setObjectName('main_button')

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.loginButton)
        hbox3.addWidget(self.cancelButton)
        hbox3.setContentsMargins(30, 0, 30, 0)

        self.registerButton = MyBtn('没有账号？立即注册！')
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.registerButton)
        hbox4.addStretch()
        hbox4.setContentsMargins(30, 0, 30, 0)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        self.FormatText()

        self.loginButton.clicked.connect(self.OnClickLoginButton)
        self.cancelButton.clicked.connect(self.close)
        self.username.returnPressed.connect(self.OnClickLoginButton)  # 文本框捕获回车键
        self.password.returnPressed.connect(self.OnClickLoginButton)  # 文本框捕获回车键

        self.setWindowOpacity(0.95)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.setStyleSheet('''
            QWidget{
                background-color:	#FFFAF0;
                border-radius:20px;
                font-family: "Microsoft YaHei", Helvetica, Arial, sans-serif;
                border-radius:15px;
            }
            QLabel#label{
                border:none;
                border-bottom:5px solid red;
                border-right:5px solid red;
                border-left:5px solid red;
                border-top:5px solid red;
                background-color:red;
                color:white;
                border-radius:10px;
            }
            QLineEdit{
                border-radius:10px;
                background-color: 	#F5F5F5;
            }
            QLineEdit:hover
            {
              background-color:	#E1FFFF;
            }
            QPushButton{
                border:none;
            }
            QPushButton#main_button:hover{
                background-color:red;
                border-left:4px solid red;
                border-right:4px solid red;
                border-top:4px solid red;
                border-bottom:4px solid red;
                border-radius:10px;
                font-weight:1000;
                color:white;
            }
        ''')

        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addLayout(vbox)
        self.setCentralWidget(self.mainWidget)  # 设置窗口主部件

    def OnClickLoginButton(self):
        """
        点击登录按钮
        :return:
        """
        try:
            # 创建新线程，使得提示框显示与其他操作并发调度
            _thread.start_new_thread(self.LoginThread, ())
        except:
            return

    def LoginThread(self):
        """
        登录线程
        :return: 无
        """
        username = self.username.text()
        password = self.password.text()
        if username == '' or password == '':
            self.WarningLabelChange('用户名或密码不能为空')
        else:
            rev = ClientLogin(username, password)
            if rev == '登录成功':
                self.signal.emit(username)
            else:
                self.WarningLabelChange(rev)

    def WarningLabelChange(self, word):
        """
        警告提示框显示字符
        :param word: 显示的字符
        :return: 无
        """
        self.warningLabel.setText(word)
        self.warningLabel.setVisible(True)
        time.sleep(3)  # 延迟三秒后消失
        self.warningLabel.setHidden(True)

    def FormatText(self):
        """
        文本字体格式设置
        """
        font = QFont()
        font.setFamily('微软雅黑')
        font.setPointSize(12)
        qSize = QSizePolicy()
        qSize.setVerticalPolicy(QSizePolicy.Maximum)
        qSize.setHorizontalPolicy(QSizePolicy.Expanding)

        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setSizePolicy(qSize)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font.setBold(False)

        font.setPointSize(12)
        reg = QRegExp('[a-zA-Z0-9]+$')  # 用户名仅限输入字母和数字
        validator = QRegExpValidator()
        validator.setRegExp(reg)
        self.username.setValidator(validator)
        self.username.setPlaceholderText('请输入您的用户名')
        self.username.setFont(font)
        self.username.setSizePolicy(qSize)
        self.username.setMaximumHeight(40)

        self.password.setPlaceholderText('请输入密码')
        self.password.setFont(font)
        self.password.setSizePolicy(qSize)
        self.password.setMaximumHeight(40)
        self.password.setEchoMode(QLineEdit.Password)

        self.loginButton.setFont(font)
        self.loginButton.setSizePolicy(qSize)
        self.loginButton.setMaximumHeight(40)
        self.loginButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.cancelButton.setFont(font)
        self.cancelButton.setSizePolicy(qSize)
        self.cancelButton.setMaximumHeight(40)
        self.cancelButton.setCursor(QCursor(Qt.PointingHandCursor))

        qSize.setHorizontalPolicy(QSizePolicy.Fixed)
        font.setPointSize(10)
        self.registerButton.setFont(font)
        self.registerButton.setMaximumHeight(40)
        self.registerButton.setStyleSheet("border:none")
        self.registerButton.setCursor(QCursor(Qt.PointingHandCursor))

        qSize.setVerticalPolicy(QSizePolicy.Fixed)
        self.warningLabel.setFont(font)
        self.warningLabel.setSizePolicy(qSize)
        self.warningLabel.setStyleSheet("color:red")
        self.warningLabel.setHidden(True)

    def Open(self):
        self.show()
        self.username.clear()
        self.password.clear()
        self.warningLabel.setHidden(True)

    def Close(self):
        self.close()


class RegisterUI(QMainWindow):
    """
    用户登录界面类
    """

    def __init__(self):
        super(RegisterUI, self).__init__()
        self.setWindowTitle('注册')  # 界面标题
        self.setFixedSize(400, 500)  # 界面大小不可变

        self.label = QLabel('欢迎注册EnglishHub')  # 应用图标
        self.label.setObjectName('label')
        self.username = QLineEdit()  # 用户名输入框
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.username)
        hbox1.setContentsMargins(30, 0, 30, 0)

        self.password = QLineEdit()  # 密码输入框
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.password)
        hbox2.setContentsMargins(30, 0, 30, 0)

        self.passwordCorrect = QLineEdit()  # 密码二次确认框
        hbox6 = QHBoxLayout()
        hbox6.addWidget(self.passwordCorrect)
        hbox6.setContentsMargins(30, 0, 30, 0)

        self.warningLabel = QLabel('提示框')  # 登录提示
        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.warningLabel)
        hbox5.addStretch()
        hbox5.setContentsMargins(30, 0, 30, 0)

        self.registerButton = QPushButton('注册')
        self.cancelButton = QPushButton('取消')
        self.registerButton.setObjectName('main_button')
        self.cancelButton.setObjectName('main_button')
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.registerButton)
        hbox3.addWidget(self.cancelButton)
        hbox3.setContentsMargins(30, 0, 30, 0)

        self.loginButton = MyBtn('已有账号？立即登录！')
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.loginButton)
        hbox4.addStretch()
        hbox4.setContentsMargins(30, 0, 30, 0)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox6)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        self.FormatText()

        self.registerButton.clicked.connect(self.OnClickRegisterButton)
        self.cancelButton.clicked.connect(self.close)
        self.username.returnPressed.connect(self.OnClickRegisterButton)  # 文本框捕获回车键
        self.password.returnPressed.connect(self.OnClickRegisterButton)  # 文本框捕获回车键
        self.passwordCorrect.returnPressed.connect(self.OnClickRegisterButton)  # 文本框捕获回车键

        self.setWindowOpacity(0.95)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.setStyleSheet('''
            QWidget{
                background-color:	#FFFAF0;
                border-radius:20px;
                font-family: "Microsoft YaHei", Helvetica, Arial, sans-serif;
                border-radius:15px;
            }
            QLabel#label{
                border:none;
                border-bottom:5px solid red;
                border-right:5px solid red;
                border-left:5px solid red;
                border-top:5px solid red;
                background-color:red;
                color:white;
                border-radius:10px;
            }
            QLineEdit{
                border-radius:10px;
                background-color: 	#F5F5F5;
            }
            QLineEdit:hover
            {
              background-color:	#E1FFFF;
            }
            QPushButton{
                border:none;
            }
            QPushButton#main_button:hover{
                background-color:red;
                border-left:4px solid red;
                border-right:4px solid red;
                border-top:4px solid red;
                border-bottom:4px solid red;
                border-radius:10px;
                font-weight:1000;
                color:white;
            }
        ''')

        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addLayout(vbox)
        self.setCentralWidget(self.mainWidget)  # 设置窗口主部件

    def OnClickRegisterButton(self):
        """
        点击注册按钮
        :return: 无
        """
        try:
            # 创建新线程，使得提示框显示与其他操作并发调度
            _thread.start_new_thread(self.RegisterThread, ())
        except:
            return

    def RegisterThread(self):
        """
        注册线程
        :return: 无
        """
        username = self.username.text()
        password = self.password.text()
        passwordCorrect = self.passwordCorrect.text()
        if username == '' or password == '' or passwordCorrect == '':
            self.WarningLabelChange('用户名或密码不能为空')
        elif len(username) > 15:
            self.WarningLabelChange('用户名长度最多为15位')
        elif len(password) < 6 or len(password) > 15:
            self.WarningLabelChange('密码长度应为6到15位')
        elif password != passwordCorrect:
            self.WarningLabelChange('两次密码输入不一致')
        else:
            rev = ClientRegister(username, password)
            self.WarningLabelChange(rev)

    def WarningLabelChange(self, word):
        """
        警告提示框显示字符
        :param word: 显示的字符
        :return: 无
        """
        self.warningLabel.setText(word)
        self.warningLabel.setVisible(True)
        time.sleep(3)  # 延迟三秒后消失
        self.warningLabel.setHidden(True)

    def FormatText(self):
        """
        文本字体格式设置
        """
        font = QFont()
        font.setFamily('微软雅黑')
        font.setPointSize(12)
        qSize = QSizePolicy()
        qSize.setVerticalPolicy(QSizePolicy.Maximum)
        qSize.setHorizontalPolicy(QSizePolicy.Expanding)

        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setSizePolicy(qSize)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font.setBold(False)

        font.setPointSize(12)
        reg = QRegExp('[a-zA-Z0-9]+$')  # 用户名仅限输入字母和数字
        validator = QRegExpValidator()
        validator.setRegExp(reg)
        self.username.setValidator(validator)
        self.username.setPlaceholderText('请输入您的用户名')
        self.username.setFont(font)
        self.username.setSizePolicy(qSize)
        self.username.setMaximumHeight(40)

        self.password.setPlaceholderText('请输入密码')
        self.password.setFont(font)
        self.password.setSizePolicy(qSize)
        self.password.setMaximumHeight(40)
        self.password.setEchoMode(QLineEdit.Password)

        self.passwordCorrect.setPlaceholderText('请再次确认密码')
        self.passwordCorrect.setFont(font)
        self.passwordCorrect.setSizePolicy(qSize)
        self.passwordCorrect.setMaximumHeight(40)
        self.passwordCorrect.setEchoMode(QLineEdit.Password)

        self.registerButton.setFont(font)
        self.registerButton.setSizePolicy(qSize)
        self.registerButton.setMaximumHeight(40)
        self.registerButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.cancelButton.setFont(font)
        self.cancelButton.setSizePolicy(qSize)
        self.cancelButton.setMaximumHeight(40)
        self.cancelButton.setCursor(QCursor(Qt.PointingHandCursor))

        qSize.setHorizontalPolicy(QSizePolicy.Fixed)
        font.setPointSize(10)
        self.loginButton.setFont(font)
        self.loginButton.setMaximumHeight(40)
        self.loginButton.setStyleSheet("border:none")
        self.loginButton.setCursor(QCursor(Qt.PointingHandCursor))

        qSize.setVerticalPolicy(QSizePolicy.Fixed)
        self.warningLabel.setFont(font)
        self.warningLabel.setSizePolicy(qSize)
        self.warningLabel.setStyleSheet("color:red")
        self.warningLabel.setHidden(True)

    def Open(self):
        self.show()
        self.username.clear()
        self.password.clear()
        self.passwordCorrect.clear()
        self.warningLabel.setHidden(True)

    def Close(self):
        self.close()


