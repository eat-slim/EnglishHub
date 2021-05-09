# 文件名称：Feedback_ui.py
# 主要功能：用户反馈功能
# ======================================================================

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Client import *
import _thread


class FeedbackUI(object):
    """
    用户反馈界面
    """
    signal = pyqtSignal(str)
    user = ''

    def setupUi(self, FeedbackUI):
        FeedbackUI.setObjectName("FeedbackUI")
        FeedbackUI.resize(979, 680)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(FeedbackUI)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(FeedbackUI)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mailLabel = QtWidgets.QLabel(self.frame)
        self.mailLabel.setObjectName("mailLabel")
        self.horizontalLayout.addWidget(self.mailLabel)
        self.mailText = QtWidgets.QLineEdit(self.frame)
        self.mailText.setObjectName("mailText")
        self.horizontalLayout.addWidget(self.mailText)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.opinionLabel = QtWidgets.QLabel(self.frame)
        self.opinionLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.opinionLabel.setObjectName("opinionLabel")
        self.horizontalLayout_2.addWidget(self.opinionLabel)
        self.opinionText = QtWidgets.QTextEdit(self.frame)
        self.opinionText.setObjectName("opinionText")
        self.horizontalLayout_2.addWidget(self.opinionText)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.sendButton = QtWidgets.QPushButton(self.frame)
        self.sendButton.setObjectName("detButton")
        self.horizontalLayout_4.addWidget(self.sendButton)
        spacerItem2 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.horizontalLayout_4.setStretch(0, 10)
        self.horizontalLayout_4.setStretch(1, 4)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 10)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 10)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_3.addWidget(self.frame)

        self.retranslateUi(FeedbackUI)
        QtCore.QMetaObject.connectSlotsByName(FeedbackUI)

        self.sendButton.clicked.connect(self.OnclickSendButton)

        self.frame.setStyleSheet('''
            QPushButton{
                border:none;
                color:black;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton:hover{
                border-bottom:5px solid red;
                font-weight:1000;
            }
            QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
            }
            QFrame{
                background:#cdcdcd;
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-right:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QTextEdit{
                background:white;
                font-size:20px;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')

    def OnclickSendButton(self):
        """
        槽函数
        :return:
        """
        if self.user == '':
            QMessageBox().warning(QWidget(), "提示", "请您先登录", QMessageBox.Yes)
            return
        add = self.mailText.text()
        text = self.opinionText.toPlainText()
        if text.strip() == '':
            QMessageBox().warning(QWidget(), "提示", "内容不能为空", QMessageBox.Yes)
            return
        elif len(text.strip()) > 200:
            QMessageBox().warning(QWidget(), "提示", "内容不能超过200个字符", QMessageBox.Yes)
            return
        if len(add) > 50:
            QMessageBox().warning(QWidget(), "提示", "联系方式不能超过50个字符", QMessageBox.Yes)
            return
        try:
            # 创建新线程
            data = {"联系方式": add, "反馈内容": text}
            _thread.start_new_thread(self.SendFeedback, (data,))
        except:
            return

    def SendFeedback(self, data):
        """
        发送反馈信息线程
        :param data: 反馈信息
        :return: 无返回值
        """
        rcv = ClientFeedback(self.user, data)
        self.signal.emit(rcv)

    def SetUser(self, username):
        """
        设置user名称
        :return:
        """
        self.user = username

    def retranslateUi(self, FeedbackUI):
        _translate = QtCore.QCoreApplication.translate
        FeedbackUI.setWindowTitle(_translate("FeedbackUI", "Form"))
        self.mailLabel.setText(_translate("FeedbackUI", "联系方式："))
        self.mailText.setPlaceholderText(_translate("FeedbackUI", "您的邮箱或手机号码(选填）"))
        self.opinionLabel.setText(_translate("FeedbackUI", "反馈意见："))
        self.opinionText.setPlaceholderText(_translate("FeedbackUI", "不多于200个字符"))
        self.sendButton.setText(_translate("FeedbackUI", "发送"))



