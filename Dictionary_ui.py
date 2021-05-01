# 文件名称：Dictionary_ui.py
# 主要功能：英汉词典翻译的界面
# 最后修改时间: 2021/04/08 21:52
# ======================================================================

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from DataBase import *
from FavoriteWords import Favorites
from WordsTest import PronunceWord

import sys

tagTrans = {'zk': '初中', 'gk': '高中', 'ky': '考研', 'ielts': '雅思', 'toefl': '托福'}
exchangeTrans = {'p': '过去式', 'd': '过去分词', 'i': '现在分词', '3': '第三人称单数', 'r': '形容词比较级',
                 't': '形容词最高级', 's': '复数', '0': '词根', '1': '词根变换形式'}


def Trans(text, dict):
    """对查询结果的简要表达方式进行替换"""
    for key in dict:
        text = text.replace(key, dict[key])
    return text


class DictionaryUI(QWidget):
    """英汉词典翻译的界面类"""

    def __init__(self):
        super(DictionaryUI, self).__init__()
        self.resize(700, 500)

        self.db = DictionaryDB('ecdict.db')  # 连接数据库

        self.searchText = QLineEdit()  # 查询框
        self.clearButton = QPushButton('清除')  # 清除键
        self.searchButton = QPushButton('查询')  # 查询键
        self.word = QLabel()  # 显示被查询单词
        self.voidLabel = QLabel()  # 占位label
        self.favoriteButton = QPushButton('收藏')  # 收藏键
        self.readWordButton = QPushButton('朗读')  # 朗读键
        self.showText = QTextEdit()  # 查询结果展示框
        self.showText.setReadOnly(True)  # 展示框只读
        # self.clearAction = QAction()
        # self.clearAction.setIcon(QStyle.SP_DialogResetButton)
        # self.searchText.addAction(self.clearAction, QLineEdit.TrailingPosition)
        # self.clearAction.triggered.connect(self.OnClickClearButton)

        self.FormatText()  # 设置文本格式

        self.searchText.returnPressed.connect(self.OnClickSearchButton)  # 文本框捕获回车键，等价于按下“查询”键
        self.clearButton.clicked.connect(self.OnClickClearButton)
        self.searchButton.clicked.connect(self.OnClickSearchButton)
        self.favoriteButton.clicked.connect(self.OnClickFavoriteButton)
        self.readWordButton.clicked.connect(self.OnclickReadWordButton)

        hBox = QHBoxLayout()  # 水平布局
        hBox.addWidget(self.searchText)
        hBox.addWidget(self.clearButton)
        hBox.addWidget(self.searchButton)

        hBox2 = QHBoxLayout()  # 水平布局
        hBox2.addWidget(self.word)
        hBox2.addWidget(self.favoriteButton)
        hBox2.addWidget(self.readWordButton)
        hBox2.addWidget(self.voidLabel)

        layout = QVBoxLayout()  # 垂直布局
        layout.addLayout(hBox)
        layout.addLayout(hBox2)
        layout.addWidget(self.showText)

        self.setLayout(layout)

    def OnClickSearchButton(self):
        """点击查询按钮"""
        wordText = self.searchText.text()  # 获取查询内容
        self.word.setText(' ' + wordText + ' ')
        searchResult = self.db.QueryWord(wordText)  # 得到查询结果
        htmlText, searchResult = self.SetTextHTML(searchResult)  # 得到查询结果的html标签
        if searchResult != {}:
            self.word.setVisible(True)
            self.favoriteButton.setVisible(True)
            self.readWordButton.setVisible(True)
            self.voidLabel.setVisible(True)
            self.SetFavoriteButton(wordText)
        else:
            self.word.setHidden(True)
            self.favoriteButton.setHidden(True)
            self.readWordButton.setHidden(True)
            self.voidLabel.setHidden(True)
        self.showText.setHtml(htmlText % searchResult)  # 展示在结果框中

    def SetFavoriteButton(self, word):
        """
        设置收藏按钮样式
        :return:
        """
        f = Favorites()
        if f.IsExist(word):
            # 收藏夹中已存在该单词
            self.favoriteButton.setText('已收藏')
        else:
            self.favoriteButton.setText('收藏')

    def OnClickFavoriteButton(self):
        """
        点击收藏按钮
        :return:
        """
        f = Favorites()
        word = self.word.text().strip()
        if self.favoriteButton.text() == '收藏':
            f.Add(word)
            self.favoriteButton.setText('已收藏')
        else:
            msgBox = QMessageBox().question(QWidget(), "询问", "确认取消收藏？", QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.No)
            if msgBox == QMessageBox.Yes:
                f.Delete(word)
                self.favoriteButton.setText('收藏')

    def OnclickReadWordButton(self):
        """
        点击朗读按钮
        :return:
        """
        PronunceWord(self.word.text().strip())

    def SetTextHTML(self, searchResult):
        """查询结果的HTML标签"""
        if searchResult is None:
            return "查无此单词", {}

        # 对部分内容重新编写格式
        tag = '|'.join(searchResult['tag'].split())
        searchResult['tag'] = Trans(tag, tagTrans)
        if searchResult['exchange'] != '':
            searchResult['exchange'] = '; '.join([exchangeTrans.get(i[0], i[0]) + i[1:] for i in searchResult['exchange'].split('/') if i[0] != '1'])
        if searchResult['collins'] is None:
            searchResult['collins'] = '无'
        if searchResult['oxford']:
            searchResult['oxford'] = '是'
        else:
            searchResult['oxford'] = '否'

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
        return htmlText, searchResult

    def OnClickClearButton(self):
        """点击清除按钮"""
        self.searchText.setText('')
        self.showText.setText('')
        self.word.setHidden(True)
        self.favoriteButton.setHidden(True)
        self.readWordButton.setHidden(True)
        self.voidLabel.setHidden(True)

    def FormatText(self):
        """文本字体格式设置"""
        font = QFont()
        font.setFamily('微软雅黑')
        font.setPointSize(10)
        self.searchText.setPlaceholderText('请输入您要查询的单词...')
        self.searchText.setFont(font)
        self.clearButton.setFont(font)
        self.searchButton.setFont(font)
        font.setPointSize(20)
        font.setBold(True)
        self.word.setFont(font)

        sizePolicy = QSizePolicy()  # 设置控件格式为水平自适应或扩展
        sizePolicy.setVerticalPolicy(QSizePolicy.Preferred)
        sizePolicy.setHorizontalPolicy(QSizePolicy.Fixed)
        self.word.setSizePolicy(sizePolicy)

        sizePolicy.setVerticalPolicy(QSizePolicy.Fixed)
        self.favoriteButton.setSizePolicy(sizePolicy)
        self.readWordButton.setSizePolicy(sizePolicy)

        sizePolicy.setHorizontalPolicy(QSizePolicy.Expanding)
        self.voidLabel.setSizePolicy(sizePolicy)

        self.word.setHidden(True)
        self.favoriteButton.setHidden(True)
        self.readWordButton.setHidden(True)
        self.voidLabel.setHidden(True)


def Dictionary_uiText():
    app = QApplication(sys.argv)
    ui = DictionaryUI()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    Dictionary_uiText()


