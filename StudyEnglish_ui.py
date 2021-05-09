# 文件名称：StudyEnglish_ui.py
# 主要功能：每日背诵的界面
# ======================================================================

from PyQt5.Qt import *
from PyQt5 import QtCore, QtWidgets
from Dictionary_ui import exchangeTrans, Trans
from StudyEnglish import *
from DataBase import *

tagTrans = {'zk': '初中词汇', 'gk': '高中词汇', 'cet4': '四级词汇', 'cet6': '六级词汇'
            , 'ky': '考研词汇', 'ielts': '雅思词汇', 'toefl': '托福词汇'}
tagTransNum = ('zk', 'gk', 'cet4', 'cet6', 'ky', 'ielts', 'toefl')


class StudyEnglishUI(object):
    """
    每日背单词的界面类
    """

    def setupUi(self, StudyEnglishUI):
        StudyEnglishUI.setObjectName("StudyEnglishUI")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(StudyEnglishUI)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.reciteFrame = QtWidgets.QFrame(StudyEnglishUI)
        self.reciteFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.reciteFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.reciteFrame.setObjectName("reciteFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.reciteFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.currentReciteLabel = QtWidgets.QLabel(self.reciteFrame)
        self.currentReciteLabel.setObjectName("currentReciteLabel")
        self.horizontalLayout_4.addWidget(self.currentReciteLabel)
        self.currentReciteLine = QtWidgets.QLineEdit(self.reciteFrame)
        self.currentReciteLine.setReadOnly(True)
        self.currentReciteLine.setObjectName("currentReciteLine")
        self.horizontalLayout_4.addWidget(self.currentReciteLine)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.resetButton = QtWidgets.QPushButton(self.reciteFrame)
        self.resetButton.setObjectName("resetButton")
        self.horizontalLayout_4.addWidget(self.resetButton)
        self.horizontalLayout_4.setStretch(0, 5)
        self.horizontalLayout_4.setStretch(1, 35)
        self.horizontalLayout_4.setStretch(2, 3)
        self.horizontalLayout_4.setStretch(3, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.ReciteButton = QtWidgets.QPushButton(self.reciteFrame)
        self.ReciteButton.setObjectName("ReciteButton")
        self.horizontalLayout_5.addWidget(self.ReciteButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.ReviewButton = QtWidgets.QPushButton(self.reciteFrame)
        self.ReviewButton.setObjectName("ReviewButton")
        self.horizontalLayout_5.addWidget(self.ReviewButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 2)
        self.horizontalLayout_5.setStretch(2, 1)
        self.horizontalLayout_5.setStretch(3, 2)
        self.horizontalLayout_5.setStretch(4, 1)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.switchFrame = QtWidgets.QFrame(self.reciteFrame)
        self.switchFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.switchFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.switchFrame.setObjectName("switchFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.switchFrame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.stackedWidget = QtWidgets.QStackedWidget(self.switchFrame)
        self.stackedWidget.setObjectName("stackedWidget")
        self.ReciteUI = QtWidgets.QWidget()
        self.ReciteUI.setObjectName("ReciteUI")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.ReciteUI)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.reciteShowWordList = QtWidgets.QListWidget(self.ReciteUI)
        self.reciteShowWordList.setObjectName("reciteShowWordList")
        self.horizontalLayout_9.addWidget(self.reciteShowWordList)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.reciteKnownButton = QtWidgets.QPushButton(self.ReciteUI)
        self.reciteKnownButton.setObjectName("reciteKnownButton")
        self.horizontalLayout_10.addWidget(self.reciteKnownButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem4)
        self.reciteVagueButton = QtWidgets.QPushButton(self.ReciteUI)
        self.reciteVagueButton.setObjectName("reciteVagueButton")
        self.horizontalLayout_10.addWidget(self.reciteVagueButton)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem5)
        self.reciteUnknownButton = QtWidgets.QPushButton(self.ReciteUI)
        self.reciteUnknownButton.setObjectName("reciteUnknownButton")
        self.horizontalLayout_10.addWidget(self.reciteUnknownButton)
        self.horizontalLayout_10.setStretch(0, 10)
        self.horizontalLayout_10.setStretch(1, 1)
        self.horizontalLayout_10.setStretch(2, 10)
        self.horizontalLayout_10.setStretch(3, 1)
        self.horizontalLayout_10.setStretch(4, 10)
        self.verticalLayout_10.addLayout(self.horizontalLayout_10)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem6)
        self.reciteDetailText = QtWidgets.QTextEdit(self.ReciteUI)
        self.reciteDetailText.setObjectName("reciteDetailText")
        self.verticalLayout_10.addWidget(self.reciteDetailText)
        self.verticalLayout_10.setStretch(0, 2)
        self.verticalLayout_10.setStretch(1, 1)
        self.verticalLayout_10.setStretch(2, 20)
        self.horizontalLayout_9.addLayout(self.verticalLayout_10)
        self.horizontalLayout_9.setStretch(0, 10)
        self.horizontalLayout_9.setStretch(1, 10)
        self.verticalLayout_8.addLayout(self.horizontalLayout_9)
        self.verticalLayout_8.setStretch(0, 10)
        self.stackedWidget.addWidget(self.ReciteUI)
        self.ReviewUI = QtWidgets.QWidget()
        self.ReviewUI.setObjectName("ReviewUI")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.ReviewUI)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.reviewShowWordList = QtWidgets.QListWidget(self.ReviewUI)
        self.reviewShowWordList.setObjectName("reviewShowWordList")
        self.horizontalLayout_11.addWidget(self.reviewShowWordList)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.reviewKnownButton = QtWidgets.QPushButton(self.ReviewUI)
        self.reviewKnownButton.setObjectName("reviewKnownButton")
        self.horizontalLayout_12.addWidget(self.reviewKnownButton)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem7)
        self.reviewVagueButton = QtWidgets.QPushButton(self.ReviewUI)
        self.reviewVagueButton.setObjectName("reviewVagueButton")
        self.horizontalLayout_12.addWidget(self.reviewVagueButton)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem8)
        self.reviewUnknownButton = QtWidgets.QPushButton(self.ReviewUI)
        self.reviewUnknownButton.setObjectName("reviewUnknownButton")
        self.horizontalLayout_12.addWidget(self.reviewUnknownButton)
        self.horizontalLayout_12.setStretch(0, 10)
        self.horizontalLayout_12.setStretch(1, 1)
        self.horizontalLayout_12.setStretch(2, 10)
        self.horizontalLayout_12.setStretch(3, 1)
        self.horizontalLayout_12.setStretch(4, 10)
        self.verticalLayout_11.addLayout(self.horizontalLayout_12)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem9)
        self.reviewDetailText = QtWidgets.QTextEdit(self.ReviewUI)
        self.reviewDetailText.setObjectName("reviewDetailText")
        self.verticalLayout_11.addWidget(self.reviewDetailText)
        self.verticalLayout_11.setStretch(0, 2)
        self.verticalLayout_11.setStretch(1, 1)
        self.verticalLayout_11.setStretch(2, 20)
        self.horizontalLayout_11.addLayout(self.verticalLayout_11)
        self.horizontalLayout_11.setStretch(0, 10)
        self.horizontalLayout_11.setStretch(1, 10)
        self.verticalLayout_5.addLayout(self.horizontalLayout_11)
        self.stackedWidget.addWidget(self.ReviewUI)
        self.verticalLayout_3.addWidget(self.stackedWidget)
        self.verticalLayout_7.addWidget(self.switchFrame)
        self.verticalLayout_2.addLayout(self.verticalLayout_7)
        self.verticalLayout_2.setStretch(0, 10)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.horizontalLayout_3.addWidget(self.reciteFrame)
        self.baseFrame = QtWidgets.QFrame(StudyEnglishUI)
        self.baseFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.baseFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.baseFrame.setObjectName("baseFrame")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.baseFrame)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem10 = QtWidgets.QSpacerItem(20, 92, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem10)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.rulesintroduction = QtWidgets.QLabel(self.baseFrame)
        self.rulesintroduction.setObjectName("rulesintroduction")
        self.verticalLayout.addWidget(self.rulesintroduction)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.choiceType = QtWidgets.QComboBox(self.baseFrame)
        self.choiceType.setObjectName("choiceType")
        self.choiceType.addItem("")
        self.choiceType.addItem("")
        self.choiceType.addItem("")
        self.choiceType.addItem("")
        self.choiceType.addItem("")
        self.choiceType.addItem("")
        self.choiceType.addItem("")
        self.choiceType.addItem("")
        self.horizontalLayout_2.addWidget(self.choiceType)
        self.choiceNum = QtWidgets.QSpinBox(self.baseFrame)
        self.choiceNum.setMinimum(10)
        self.choiceNum.setMaximum(100)
        self.choiceNum.setSingleStep(5)
        self.choiceNum.setObjectName("choiceNum")
        self.horizontalLayout_2.addWidget(self.choiceNum)
        self.choiceOrder = QtWidgets.QComboBox(self.baseFrame)
        self.choiceOrder.setObjectName("choiceOrder")
        self.choiceOrder.addItem("")
        self.choiceOrder.addItem("")
        self.choiceOrder.addItem("")
        self.horizontalLayout_2.addWidget(self.choiceOrder)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.startRectieButton = QtWidgets.QPushButton(self.baseFrame)
        self.startRectieButton.setObjectName("startRectieButton")
        self.verticalLayout.addWidget(self.startRectieButton)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        self.horizontalLayout_7.setStretch(0, 10)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        spacerItem11 = QtWidgets.QSpacerItem(20, 187, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem11)
        self.verticalLayout_6.setStretch(0, 1)
        self.verticalLayout_6.setStretch(1, 3)
        self.verticalLayout_6.setStretch(2, 1)
        self.horizontalLayout_3.addWidget(self.baseFrame)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)

        self.retranslateUi(StudyEnglishUI)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(StudyEnglishUI)

        self.DecideFrame()

        self.reviewUnknownButton.setHidden(True)
        self.reviewVagueButton.setHidden(True)
        self.reviewKnownButton.setHidden(True)
        self.reciteUnknownButton.setHidden(True)
        self.reciteVagueButton.setHidden(True)
        self.reciteKnownButton.setHidden(True)

        self.reciteShowWordList.itemClicked.connect(self.ReciteWordDetail)
        self.reviewShowWordList.itemClicked.connect(self.ReviewWordDetail)

        self.ReciteButton.clicked.connect(self.OnClickButton1)
        self.ReviewButton.clicked.connect(self.OnClickButton2)
        self.startRectieButton.clicked.connect(self.StartRecite)
        self.resetButton.clicked.connect(self.ResetWord)
        self.reciteKnownButton.clicked.connect(self.ReciteKnown)
        self.reviewKnownButton.clicked.connect(self.ReviewKnown)
        self.reciteVagueButton.clicked.connect(self.ReciteVague)
        self.reviewVagueButton.clicked.connect(self.ReviewVague)
        self.reciteUnknownButton.clicked.connect(self.ReciteUnknown)
        self.reviewUnknownButton.clicked.connect(self.ReviewUnknown)

        self.baseFrame.setStyleSheet('''
            QPushButton{
                border:none;
                font-size:15px;
                font-weight:700;
                font-family: "微软雅黑", Helvetica, Arial, sans-serif;
            }
            QPushButton:hover{
                border-top:2px solid red;
                border-bottom:2px solid red;
                border-right:4px solid red;
                border-left:4px solid red;
                border-radius:5px;
                font-weight:800;
                background:red;
                color:black;
            }
            QFrame{
                background:gray;
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-right:1px solid white;
                border-radius:10px;
            }
            QLabel{
                font-size:20px;
                font-family: "微软雅黑", Helvetica, Arial, sans-serif;
            }
            QSpinBox{
                color:black;
                font-family: "微软雅黑", Helvetica, Arial, sans-serif;
                border-radius:5px;
                background::#232C51;
            }
            QComboBox{
                color:black;
                font-family: "微软雅黑", Helvetica, Arial, sans-serif;
                border-radius:5px;
                background::#232C51;
            }
            
        ''')

        self.reciteFrame.setStyleSheet('''
                    QPushButton{
                        border:none;
                        color:#707070;
                        font-size:18px;
                        font-weight:500;
                        font-family: "微软雅黑", Helvetica, Arial, sans-serif;
                    }
                    QLabel{
                        border:none;
                        border-bottom:1px solid white;
                        font-size:30px;
                        font-weight:700;
                        font-family: "微软雅黑", Helvetica, Arial, sans-serif;
                    }
                    QLabel#currentReciteLabel{
                        border:2px solid black;
                    }
                    QPushButton:hover{
                        background-color:red;
                        color:white;
                        border-right:4px solid red;
                        border-left:4px solid red;
                        border-top:4px solid red;
                        border-bottom:4px solid red;
                        font-weight:1000;
                        border-radius:10px;
                    }
                    QLineEdit{
                        border:1px solid gray;
                        width:800px;
                        border-radius:10px;
                        padding:2px 4px;
                        background:#cdcdcd;
                        color:red;
                        font-size:20px;
                        font-family: "微软雅黑", Helvetica, Arial, sans-serif;

                    }
                    QTextEdit{
                        background-color:#cdcdcd;
                        border:1px solid gray;
                        width:300px;
                        border-radius:10px;
                        padding:2px 4px
                    }
                    QListWidget{
                        border-radius:10px;
                        background-color:#cdcdcd;
                        border:1px solid gray;
                        width:300px;
                        border-radius:10px;
                        padding:2px 4px;
                    }
                ''')

    def retranslateUi(self, StudyEnglishUI):
        _translate = QtCore.QCoreApplication.translate
        StudyEnglishUI.setWindowTitle(_translate("StudyEnglishUI", "Form"))
        self.currentReciteLabel.setText(_translate("StudyEnglishUI", "当前学习："))
        self.resetButton.setText(_translate("StudyEnglishUI", "重置学习内容"))
        self.ReciteButton.setText(_translate("StudyEnglishUI", "学习今日单词"))
        self.ReviewButton.setText(_translate("StudyEnglishUI", "复习昨日生词"))
        self.reciteKnownButton.setText(_translate("StudyEnglishUI", "known"))
        self.reciteVagueButton.setText(_translate("StudyEnglishUI", "vague"))
        self.reciteUnknownButton.setText(_translate("StudyEnglishUI", "unknown"))
        self.reviewKnownButton.setText(_translate("StudyEnglishUI", "known"))
        self.reviewVagueButton.setText(_translate("StudyEnglishUI", "vague"))
        self.reviewUnknownButton.setText(_translate("StudyEnglishUI", "unknown"))
        html = """
                    <html><head/><body><p>学习单词规则：</p>
                    <p>1、将单词分为三个等级，来区分单词的熟悉度</p>
                    <p>2、每日可新学习规定单词，也会要求复习昨日不熟悉单词，加深印象</p>
                    <p>3、每次学习单词会从上次离开处重新开始，且复习之后出现不熟悉单词</p>
                    <p>4、Don\'t lose faith, as long as the unremittingly, you will get some fruits</p>
                    <p><br/>请选择学习的内容</p></body></html>
                """
        self.rulesintroduction.setText(_translate("StudyEnglishUI", html))
        self.choiceType.setItemText(0, _translate("StudyEnglishUI", "选择要学习的词库"))
        self.choiceType.setItemText(1, _translate("StudyEnglishUI", "中考词汇"))
        self.choiceType.setItemText(2, _translate("StudyEnglishUI", "高考词汇"))
        self.choiceType.setItemText(3, _translate("StudyEnglishUI", "四级词汇"))
        self.choiceType.setItemText(4, _translate("StudyEnglishUI", "六级词汇"))
        self.choiceType.setItemText(5, _translate("StudyEnglishUI", "考研词汇"))
        self.choiceType.setItemText(6, _translate("StudyEnglishUI", "雅思词汇"))
        self.choiceType.setItemText(7, _translate("StudyEnglishUI", "托福词汇"))
        self.choiceOrder.setItemText(0, _translate("StudyEnglishUI", "选择顺序"))
        self.choiceOrder.setItemText(1, _translate("StudyEnglishUI", "乱序"))
        self.choiceOrder.setItemText(2, _translate("StudyEnglishUI", "顺序"))
        self.startRectieButton.setText(_translate("StudyEnglishUI", "开始学习"))

    def CreateReciteFrame(self):
        self.baseFrame.setHidden(True)
        self.reciteFrame.setVisible(True)
        self.currentReciteLine.setText(self.ReadConfig())
        self.ReviewCreateListItem()
        self.ReciteCreateListItem()

    def CreateBaseFrame(self):
        self.baseFrame.setVisible(True)
        self.reciteFrame.setHidden(True)

    def ResetWord(self):
        msgBox = QMessageBox().question(QWidget(), "询问", "确认重置单词？", QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
        if msgBox == QMessageBox.Yes:
            with open(config, 'w') as configFile:
                configFile.truncate()
            self.reciteFrame.setHidden(True)
            self.baseFrame.setVisible(True)
            if os.path.exists('Data\\studyRecord'):
                shutil.rmtree('Data\\studyRecord')

    def ReadConfig(self):
        with open(config, 'r') as configFile:
            configList = [i.strip() for i in configFile.readlines()]
        category = Trans(configList[0], tagTrans)
        dailyNumber = configList[1]
        sequence = int(configList[2])
        if sequence:
            sequence = '顺序'
        else:
            sequence = '乱序'
        configList = category + " 每日 " + dailyNumber + ' 词 '+sequence
        return configList

    def ReciteCreateListItem(self):
        recite = ReciteWords()
        l = recite.DailyRecite()
        if l:
            font = QFont()
            font.setFamily('微软雅黑')
            font.setBold(True)
            font.setPointSize(12)
            qSize = QSizePolicy()
            qSize.setHorizontalPolicy(QSizePolicy.Ignored)
            self.reciteShowWordList.clear()
            for i in l:
                item = QListWidgetItem()  # 列表项目
                item.setSizeHint(QSize(0, 50))

                wordStyle = QWidget()  # 列表项的布局方式
                wordTextLabel = QLabel()  # 单词文本
                wordTextLabel.setFont(font)
                item.setText(' ' + i)
                item.setFont(font)

                hbox = QHBoxLayout()
                hbox.addWidget(wordTextLabel)

                wordStyle.setLayout(hbox)  # 水平布局
                self.reciteShowWordList.addItem(item)
                self.reciteShowWordList.setItemWidget(item, wordStyle)

    def ReviewCreateListItem(self):
        review = ReciteWords()
        l = review.DailyReview()
        if l:
            font = QFont()
            font.setFamily('微软雅黑')
            font.setBold(True)
            font.setPointSize(12)
            qSize = QSizePolicy()
            qSize.setHorizontalPolicy(QSizePolicy.Ignored)
            self.reviewShowWordList.clear()
            for i in l:
                item = QListWidgetItem()  # 列表项目
                item.setSizeHint(QSize(0, 50))

                wordStyle = QWidget()  # 列表项的布局方式
                wordTextLabel = QLabel()  # 单词文本
                wordTextLabel.setFont(font)
                item.setText(' ' + i)
                item.setFont(font)

                hbox = QHBoxLayout()
                hbox.addWidget(wordTextLabel)

                wordStyle.setLayout(hbox)  # 水平布局
                self.reviewShowWordList.addItem(item)
                self.reviewShowWordList.setItemWidget(item, wordStyle)

    def ReciteWordDetail(self, item):
        itemWord = item.text()[1:]  # 获取查询内容
        db = DictionaryDB(dictionaryDB)
        detail = db.QueryWord(itemWord)  # 得到查询结果
        if detail is not None:
            # 对部分内容重新编写格式
            tag = '|'.join(detail['tag'].split())
            detail['tag'] = Trans(tag, tagTrans)
            if detail['exchange'] != '':
                detail['exchange'] = '; '.join(
                    [exchangeTrans.get(i[0], i[0]) + i[1:] for i in detail['exchange'].split('/') if i[0] != '1'])
            if detail['collins'] is None:
                detail['collins'] = '无'
            if detail['oxford']:
                detail['oxford'] = '是'
            else:
                detail['oxford'] = '否'
            htmlText = """
                            <h1>%(word)s</h1>
                            <h3>/%(phonetic)s/</h3>
                            <hr>
                            <h3>%(definition)s</h3>
                            <h2>%(translation)s</h2>
                            <h3>柯林斯星级:%(collins)s</h3>
                            <h3>牛津三千核心词汇:%(oxford)s</h3>
                            <h3>%(tag)s</h3>
                            <h3>%(exchange)s</h3>
                        """
            self.reciteDetailText.setHtml(htmlText % detail)  # 展示在结果框中
            self.reciteKnownButton.setVisible(True)
            self.reciteVagueButton.setVisible(True)
            self.reciteUnknownButton.setVisible(True)
        else:
            self.reciteDetailText.setText('无详细释义')

    def ReviewWordDetail(self, item):
        itemWord = item.text()[1:]  # 获取查询内容
        db = DictionaryDB(dictionaryDB)
        detail = db.QueryWord(itemWord)  # 得到查询结果
        if detail is not None:
            # 对部分内容重新编写格式
            tag = '|'.join(detail['tag'].split())
            detail['tag'] = Trans(tag, tagTrans)
            if detail['exchange'] != '':
                detail['exchange'] = '; '.join(
                    [exchangeTrans.get(i[0], i[0]) + i[1:] for i in detail['exchange'].split('/') if i[0] != '1'])
            if detail['collins'] is None:
                detail['collins'] = '无'
            if detail['oxford']:
                detail['oxford'] = '是'
            else:
                detail['oxford'] = '否'
            htmlText = """
                            <h1>%(word)s</h1>
                            <h3>/%(phonetic)s/</h3>
                            <hr>
                            <h3>%(definition)s</h3>
                            <h2>%(translation)s</h2>
                            <h3>柯林斯星级:%(collins)s</h3>
                            <h3>牛津三千核心词汇:%(oxford)s</h3>
                            <h3>%(tag)s</h3>
                            <h3>%(exchange)s</h3>
                        """
            self.reviewDetailText.setHtml(htmlText % detail)  # 展示在结果框中
            self.reviewKnownButton.setVisible(True)
            self.reviewVagueButton.setVisible(True)
            self.reviewUnknownButton.setVisible(True)
        else:
            self.reviewDetailText.setText('无详细释义')

    def ReciteKnown(self, item):
        itemWord = self.reciteDetailText.toPlainText()  # 获取查询内容
        word = itemWord.split()[0]
        recite = ReciteWords()
        recite.ReciteWord(word, "known")
        word = self.reciteShowWordList.currentItem()
        row = self.reciteShowWordList.currentRow()
        items = QListWidgetItem(word)
        color = QColor()
        color.setRgb(255, 182, 193)
        brush = QBrush(color)
        items.setBackground(brush)
        self.reciteShowWordList.takeItem(row)
        self.reciteShowWordList.insertItem(row, items)

    def ReciteVague(self):
        itemWord = self.reciteDetailText.toPlainText()  # 获取查询内容
        word = itemWord.split()[0]
        recite = ReciteWords()
        recite.ReciteWord(word, "vague")
        word = self.reciteShowWordList.currentItem()
        row = self.reciteShowWordList.currentRow()
        items = QListWidgetItem(word)
        color = QColor()
        color.setRgb(255, 182, 193)
        brush = QBrush(color)
        items.setBackground(brush)
        self.reciteShowWordList.takeItem(row)
        self.reciteShowWordList.insertItem(row, items)

    def ReciteUnknown(self):
        itemWord = self.reciteDetailText.toPlainText()  # 获取查询内容
        word = itemWord.split()[0]
        recite = ReciteWords()
        recite.ReciteWord(word, "unknown")
        word = self.reciteShowWordList.currentItem()
        row = self.reciteShowWordList.currentRow()
        items = QListWidgetItem(word)
        color = QColor()
        color.setRgb(255, 182, 193)
        brush = QBrush(color)
        items.setBackground(brush)
        self.reciteShowWordList.takeItem(row)
        self.reciteShowWordList.insertItem(row, items)

    def ReviewKnown(self):
        itemWord = self.reviewDetailText.toPlainText()  # 获取查询内容
        word = itemWord.split()[0]
        recite = ReciteWords()
        recite.ReviewWord(word, "known")
        word = self.reviewShowWordList.currentItem()
        row = self.reviewShowWordList.currentRow()
        items = QListWidgetItem(word)
        color = QColor()
        color.setRgb(255, 182, 193)
        brush = QBrush(color)
        items.setBackground(brush)
        self.reviewShowWordList.takeItem(row)
        self.reviewShowWordList.insertItem(row, items)

    def ReviewVague(self):
        itemWord = self.reviewDetailText.toPlainText()  # 获取查询内容
        word = itemWord.split()[0]
        recite = ReciteWords()
        recite.ReviewWord(word, "vague")
        word = self.reviewShowWordList.currentItem()
        row = self.reviewShowWordList.currentRow()
        items = QListWidgetItem(word)
        color = QColor()
        color.setRgb(255, 182, 193)
        brush = QBrush(color)
        items.setBackground(brush)
        self.reviewShowWordList.takeItem(row)
        self.reviewShowWordList.insertItem(row, items)

    def ReviewUnknown(self):
        itemWord = self.reviewDetailText.toPlainText()  # 获取查询内容
        word = itemWord.split()[0]
        recite = ReciteWords()
        recite.ReviewWord(word, "unknown")
        word = self.reviewShowWordList.currentItem()
        row = self.reviewShowWordList.currentRow()
        items = QListWidgetItem(word)
        color = QColor()
        color.setRgb(255, 182, 193)
        brush = QBrush(color)
        items.setBackground(brush)
        self.reviewShowWordList.takeItem(row)
        self.reviewShowWordList.insertItem(row, items)

    def OnClickButton1(self):
        if self.stackedWidget.currentIndex() != 0:
            self.stackedWidget.setCurrentIndex(0)

    def OnClickButton2(self):
        if self.stackedWidget.currentIndex() != 1:
            self.stackedWidget.setCurrentIndex(1)

    def StartRecite(self):
        wordType = self.choiceType.currentIndex()
        dailyNumber = self.choiceNum.value()
        wordOrder = self.choiceOrder.currentIndex()
        if wordType == 0 or wordOrder == 0:
            QMessageBox.about(QWidget(), "提示", "请选择正确的词库或顺序")
        else:
            wordType = tagTransNum[wordType-1]
            wordOrder -= 1
            ReciteWords(wordType, dailyNumber, wordOrder)
            self.CreateReciteFrame()

    def DecideFrame(self):
        if os.path.exists(config):
            size = os.path.getsize(config)
            if size == 0:
                self.CreateBaseFrame()
            else:
                self.CreateReciteFrame()
        else:
            self.CreateBaseFrame()


