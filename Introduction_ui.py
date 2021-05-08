# 文件名称：Introduction.py
# 主要功能：程序介绍
# ======================================================================

from PyQt5 import QtCore, QtWidgets


class Ui_IntroductionUI(object):
    """
    程序介绍界面
    """

    def setupUi(self, IntroductionUI):
        IntroductionUI.setObjectName("IntroductionUI")
        IntroductionUI.resize(651, 521)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(IntroductionUI)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(IntroductionUI)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout_2.addWidget(self.frame)

        self.retranslateUi(IntroductionUI)
        QtCore.QMetaObject.connectSlotsByName(IntroductionUI)

        self.frame.setStyleSheet('''
                    QLabel{
                        color:black;
                        font-size:20px;
                        font-weight:500;
                        font-family:'微软雅黑';  
                    }
                ''')

    def retranslateUi(self, IntroductionUI):
        _translate = QtCore.QCoreApplication.translate
        IntroductionUI.setWindowTitle(_translate("IntroductionUI", "Form"))
        # html = """
        #     <html><head/>
        #         <body><p align=\"center\">欢迎使用，我们设计的EnglishHub</p>
        #         <p align=\"center\"><br/></p>
        #         <p align=\"center\">我们是来自东北大学计算机专业五人组</p>
        #         <p align=\"center\"><br/></p>
        #         <p align=\"center\">这是我们一起完成的基于小牛翻译的EnglishHub</p>
        #         <p align=\"center\"><br/></p><p align=\"center\">虽然它目前并不是一个完美的产品</p>
        #         <p align=\"center\"><br/></p><p align=\"center\">但之后，我们会不断地去完善它，希望他最终有一个完整的ending</p>
        #         <p align=\"center\"><br/></p><p align=\"center\">我们之中有半神，也有废物，不过</p>
        #         <p align=\"center\"><br/></p><p align=\"center\">我们是一群热爱计算机的学生，并为成为一名优秀的CS人不断努力着！</p>
        #     </body></html>
        # """
        html = """
            <html><head/>
                <body><p align=\"center\">欢迎使用EnglishHub</p>
                <p align=\"center\"><hr/></p>
                <p align=\"center\">我们是来自东北大学计算机专业的五人小组</p>
                <p align=\"center\">丁子恒 张钊源 陈俊江 罗巍耀 高一峰（按姓氏笔画顺序排列）</p>
                <p align=\"center\">这是我们一起完成的英文学习软件</p>
                <p align=\"center\"><hr/></p>
                <p align=\"center\">他现在的功能有</p>
                <p align=\"center\">基于小牛翻译API的：在线翻译</p>
                <p align=\"center\">基于开源英汉词典的：单词查询</p>
                <p align=\"center\">依赖sqlite3数据库的：每日背单词、单词收藏</p>
                <p align=\"center\">基于HTTP请求的：每日新闻</p>
                <p align=\"center\">使用C/S架构、TCP协议+多线程的网络通信：注册、登录以及反馈</p>
                <p align=\"center\"><hr/></p>
                <p align=\"center\">虽然他目前并不是一个完美的产品</p>
                <p align=\"center\">但之后，我们会不断地去完善他，希望他最终有一个完整的ending</p>
                <p align=\"center\">我们之中有半神，也有菜鸟，不过</p>
                <p align=\"center\">我们是一群热爱计算机的学生，并向着成为一名优秀的CS人而不断努力着！</p>
            </body></html>
                """
        self.label.setText(_translate("IntroductionUI", html))
