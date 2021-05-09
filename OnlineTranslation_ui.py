# 文件名称：OnlineTranslation_ui.py
# 主要功能：在线文本英汉互译的界面
# ======================================================================

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from OnlineTranslation import *


class OnlineTranslationUI(object):
    """
    在线翻译模块的界面类
    """

    usable = False

    def setupUi(self, OnlineTranslationUI):
        OnlineTranslationUI.setObjectName("OnlineTranslationUI")
        OnlineTranslationUI.resize(875, 673)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(OnlineTranslationUI)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(OnlineTranslationUI)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.inputText = QtWidgets.QTextEdit(self.frame)
        self.inputText.setObjectName("inputText")
        self.verticalLayout.addWidget(self.inputText)
        self.transButton = QtWidgets.QPushButton(self.frame)
        self.transButton.setAccessibleName("")
        self.transButton.setObjectName("transButton")
        self.transZhButton = QtWidgets.QPushButton(self.frame)
        self.transZhButton.setAccessibleName("")
        self.transZhButton.setObjectName("transZhButton")

        hbox = QHBoxLayout()
        hbox.addWidget(self.transButton)
        hbox.addWidget(self.transZhButton)

        self.verticalLayout.addLayout(hbox)
        self.outputText = QtWidgets.QTextEdit(self.frame)
        self.outputText.setObjectName("outputText")
        self.verticalLayout.addWidget(self.outputText)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addWidget(self.frame)

        self.retranslateUi(OnlineTranslationUI)
        QtCore.QMetaObject.connectSlotsByName(OnlineTranslationUI)

        self.FormatText()  # 设置文字格式

        self.transButton.clicked.connect(self.OnClickTransButton)  # 翻译按钮连接信号槽
        self.transZhButton.clicked.connect(self.OnClickTransZhButton)

        self.frame.setStyleSheet('''
            QPushButton{
                border:none;
                color:black;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton:hover{
                border-left:2zpx solid red;
                border-right:2px solid red;
                border-top:1px solid red;
                border-bottom:1px solid red;
                background:black;
                color:white;
                font-weight:1000;
                border-radius:5px;
            }
            QFrame{
                background:#cdcdcd;
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-right:1px solid white;
                border-radius:10px;
            }
        ''')

    def retranslateUi(self, OnlineTranslationUI):
        _translate = QtCore.QCoreApplication.translate
        OnlineTranslationUI.setWindowTitle(_translate("OnlineTranslationUI", "Form"))
        self.transButton.setText(_translate("OnlineTranslationUI", "中译英"))
        self.transZhButton.setText(_translate("OnlineTranslationUI", "英译中"))

    def ErrorCodeProcess(self, errorCode):
        """根据翻译API回传的错误代码进行不同的错误处理"""
        # 请求出现错误，进入错误处理
        if errorCode == 'empty':
            return
        elif errorCode == 'too long':
            text = "文本长度超出1500字"
        elif errorCode == 'network anomaly':
            text = "网络异常"
        elif errorCode == 10001:
            text = "请求频繁"
        elif errorCode == 13007:
            text = "语言不支持"
        elif errorCode == 13008:
            text = "请求超时"
        else:
            text = "查询失败，请重试"
        QMessageBox().warning(QWidget(), "警告", text, QMessageBox.Yes)

    def OnClickTransButton(self):
        """点击查询按钮，进行翻译"""
        if not self.usable:
            QMessageBox().warning(QWidget(), "提示", "请您先登录", QMessageBox.Yes)
            return
        # 获取输入信息，并调用翻译模块
        sourceText = self.inputText.toPlainText()
        res_dict = Translate(sourceText, transType=0)

        # 异常处理
        if "error_code" in res_dict:
            self.ErrorCodeProcess(res_dict["error_code"])
            result = ""
        # 获取API回传的翻译结果
        else:
            result = res_dict.get("tgt_text", "")
        self.outputText.setPlainText(result)

    def OnClickTransZhButton(self):
        """点击查询按钮，进行翻译"""
        if not self.usable:
            QMessageBox().warning(QWidget(), "提示", "请您先登录", QMessageBox.Yes)
            return
        # 获取输入信息，并调用翻译模块
        sourceText = self.inputText.toPlainText()
        res_dict = Translate(sourceText, transType=1)

        # 异常处理
        if "error_code" in res_dict:
            self.ErrorCodeProcess(res_dict["error_code"])
            result = ""
        # 获取API回传的翻译结果
        else:
            result = res_dict.get("tgt_text", "")
        self.outputText.setPlainText(result)

    def FormatText(self):
        """文本字体格式设置"""
        font = QFont()
        font.setFamily('微软雅黑')
        font.setPointSize(12)
        self.inputText.setFont(font)
        self.outputText.setFont(font)
        self.transButton.setFont(font)
        self.outputText.setReadOnly(True)

    def SetUsable(self, usable):
        """
        设置功能可用性
        :return:
        """
        self.usable = usable



