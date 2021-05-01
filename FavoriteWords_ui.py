# 文件名称：FavoriteWords_ui.py
# 主要功能：收藏夹的界面
# 最后修改时间: 2021/04/28 21:52
# ======================================================================

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from FavoriteWords import *
import sys
import time

from DataBase import *
from Dictionary_ui import exchangeTrans, tagTrans, Trans


class FavoriteWordsUI(QWidget):
    """单词收藏夹界面"""

    def __init__(self):
        super(FavoriteWordsUI, self).__init__()
        self.resize(700, 500)

        self.controlStrip = QHBoxLayout()  # 功能栏水平布局
        self.button1 = QPushButton('刷新')
        self.button2 = QPushButton('取消收藏')
        self.button3 = QPushButton('全部取消收藏')
        self.controlStrip.addWidget(self.button1)
        self.controlStrip.addWidget(self.button2)
        self.controlStrip.addWidget(self.button3)
        self.button1.clicked.connect(self.Refresh)
        self.button2.clicked.connect(self.UnFavorite)
        self.button3.clicked.connect(self.UnFavoriteAll)

        self.details = QHBoxLayout()  # 具体内容为水平布局
        self.showStrip = QListWidget()  # 单词展示栏为列表
        self.showStrip.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.CreateListItem()
        self.detailText = QTextEdit()  # 具体释义界面
        self.closeButton = QPushButton('关闭')  # 关闭具体释义
        qSize = QSizePolicy()
        qSize.setHorizontalPolicy(QSizePolicy.Fixed)
        self.closeButton.setSizePolicy(qSize)
        vboxDetail = QVBoxLayout()
        vboxDetail.addWidget(self.closeButton)
        vboxDetail.addWidget(self.detailText)
        self.details.addWidget(self.showStrip)
        self.details.addLayout(vboxDetail)
        self.closeButton.clicked.connect(self.CloseWordDetaile)
        self.showStrip.itemDoubleClicked.connect(self.WordDetail)
        self.detailText.setHidden(True)
        self.closeButton.setHidden(True)

        vbox = QVBoxLayout()  # 整体为垂直布局
        vbox.addLayout(self.controlStrip)
        vbox.addLayout(self.details)
        self.setLayout(vbox)

    def CreateListItem(self):
        """
        根据收藏夹内容填充列表内容
        :return:
        """
        db = DictionaryDB(dbFile)
        f = Favorites()
        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)
        font.setPointSize(12)
        qSize = QSizePolicy()
        qSize.setHorizontalPolicy(QSizePolicy.Ignored)
        for i in f.Show():
            item = QListWidgetItem()  # 列表项目
            item.setSizeHint(QSize(0, 50))

            wordStyle = QWidget()  # 列表项的布局方式
            wordTextLabel = QLabel()  # 单词文本
            # wordTextLabel.setFont(font)
            item.setText(' ' + i)
            item.setFont(font)

            wordTranslation = db.QueryWord(i).get('translation', '')  # 单词翻译
            wordTranslation = (' '.join(wordTranslation.split()))
            if len(wordTranslation) > 30:
                wordTranslation = wordTranslation[:30] + '...'
            wordTranslationLabel = QLabel(wordTranslation)
            wordTranslationLabel.setSizePolicy(qSize)

            # button = QPushButton('取消收藏')  # 取消收藏的按钮
            # button.clicked.connect(lambda: self.UnFavorite(i))

            hbox = QHBoxLayout()
            hbox.addWidget(wordTextLabel)
            hbox.addWidget(wordTranslationLabel)
            # hbox.addWidget(button)
            # hbox.setStretch(0, 3)
            # hbox.setStretch(1, 6)
            # hbox.setStretch(2, 1)

            wordStyle.setLayout(hbox)  # 水平布局
            self.showStrip.addItem(item)
            self.showStrip.setItemWidget(item, wordStyle)

    def WordDetail(self, item):
        """
        展示单词详细释义
        :return:
        """
        self.detailText.setVisible(True)
        self.closeButton.setVisible(True)
        itemWord = item.text()[1:]  # 获取查询内容
        db = DictionaryDB('ecdict.db')
        detail = db.QueryWord(itemWord)  # 得到查询结果
        if detail != None:
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
            self.detailText.setHtml(htmlText % detail)  # 展示在结果框中
        else:
            self.detailText.setText('无详细释义')

    def CloseWordDetaile(self):
        """
        关闭详细释义界面
        :return:
        """
        self.detailText.setHidden(True)
        self.closeButton.setHidden(True)

    def Refresh(self):
        """
        刷新收藏夹内容
        :return:
        """
        self.showStrip.clear()
        self.CreateListItem()

    def UnFavorite(self):
        """
        取消收藏
        :return:
        """
        f = Favorites()
        index = self.showStrip.selectedItems()
        if len(index):
            msgBox = QMessageBox().question(QWidget(), "询问", "确认取消收藏？", QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.No)
            if msgBox == QMessageBox.Yes:
                for i in index:
                    f.Delete(i.text()[1:])
                self.Refresh()

    def UnFavoriteAll(self):
        """
        全部取消收藏
        :return:
        """
        msgBox = QMessageBox().question(QWidget(), "询问", "确认全部取消收藏？", QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
        if msgBox == QMessageBox.Yes:
            f = Favorites()
            f.DeleteAll()
            self.Refresh()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = FavoriteWordsUI()
    main.show()
    sys.exit(app.exec_())







