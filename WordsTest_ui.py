# 文件名称：WordsTest_ui.py
# 主要功能：单词测试功能的界面
# 最后修改时间: 2021/04/27 16:19
# ======================================================================


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from OnlineTranslation import *
import sys

from WordsTest import WordsForTest

transType = {'当前已学习单词': 'study', '中考词汇': 'zk', '高考词汇': 'gk', '四级词汇': 'cet4',
             '六级词汇': 'cet6', '考研词汇': 'ky', '雅思词汇': 'ielts', '托福词汇': 'toefl'}


class WordsForTestUI(QWidget):
    """单词测试的界面"""

    def __init__(self):
        super(WordsForTestUI, self).__init__()
        self.resize(700, 500)

        vbox = QVBoxLayout()
        self.setLayout(vbox)
        self.initTest = QVBoxLayout()  # 选择测试内容
        self.showTest = QVBoxLayout()  # 测试界面
        vbox.addLayout(self.initTest)
        vbox.addLayout(self.showTest)

        # 测试内容初始化界面
        self.startTestLabel = QLabel('请选择测试内容')
        startTestHbox = QHBoxLayout()  # 选择区域
        self.startTestButton = QPushButton('开始测试')
        self.choiceType = QComboBox()  # 下拉框
        self.choiceNum = QSpinBox()  # 数量选择框
        startTestHbox.addWidget(self.choiceType)
        startTestHbox.addWidget(self.choiceNum)
        self.initTest.addWidget(self.startTestLabel)
        self.initTest.addLayout(startTestHbox)
        self.initTest.addWidget(self.startTestButton)

        qSize = QSizePolicy()
        qSize.setVerticalPolicy(QSizePolicy.Fixed)
        self.startTestLabel.setSizePolicy(qSize)
        self.startTestLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.choiceType.addItems(['当前已学习单词', '中考词汇', '高考词汇',
                                  '四级词汇', '六级词汇', '考研词汇', '雅思词汇', '托福词汇'])
        self.choiceNum.setRange(5, 50)  # 测试范围5-50个单词
        self.choiceNum.setSingleStep(5)  # 步长5
        self.choiceNum.setValue(20)  # 初始值为20

        # 测试单词界面






        self.nextWordButton = QPushButton('下一个')
        self.startTestButton.clicked.connect(self.OnClickStartTestButton)
        self.nextWordButton.clicked.connect(self.OnClickNextWordButton)

        self.initTest.addWidget(self.startTestButton)
        self.showTest.addWidget(self.nextWordButton)

        self.Format()

    def Format(self):
        """
        设置控件格式
        :return:
        """
        self.nextWordButton.setHidden(True)

    def OnClickStartTestButton(self):
        """
        选择完成后开始测试
        :return:
        """
        self.startTestButton.setHidden(True)
        self.nextWordButton.setVisible(True)


    def OnClickNextWordButton(self):
        """
        继续测试下一个单词
        :return:
        """
        self.nextWordButton.setHidden(True)
        self.startTestButton.setVisible(True)



