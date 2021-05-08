# 文件名称：FavoriteWords_ui.py
# 主要功能：收藏夹的界面
# ======================================================================
import qtawesome
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from FavoriteWords import *

from DataBase import *
from Dictionary_ui import exchangeTrans, tagTrans, Trans


class FavoriteWordsUI(QWidget):
    """单词收藏夹界面"""

    def __init__(self):
        super(FavoriteWordsUI, self).__init__()
        self.resize(700, 500)

        self.controlStrip = QHBoxLayout()  # 功能栏水平布局
        self.button1 = QPushButton(qtawesome.icon('fa.refresh', color='black'), '刷新')
        self.button2 = QPushButton(qtawesome.icon('fa.star-half-o', color='black'), '取消收藏')
        self.button3 = QPushButton(qtawesome.icon('fa.star-o', color='black'), '全部取消收藏')
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
        self.closeButton = QPushButton(qtawesome.icon('fa.times', color='black'), '关闭')  # 关闭具体释义
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

        self.setStyleSheet('''
            QPushButton{
                border:none;
                color:#707070;
                font-size:18px;
                font-weight:500;
                font-family: "微软雅黑", Helvetica, Arial, sans-serif;
            }
            QPushButton:hover{
                background-color:#cdcdcd;
                color:red;
                border-right:4px solid red;
                border-left:4px solid red;
                font-weight:1000;
            }
            QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
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

    def CreateListItem(self):
        """
        根据收藏夹内容填充列表内容
        :return:
        """
        db = DictionaryDB(dictionaryDB)
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
            item.setText(' ' + i)
            item.setFont(font)

            wordTranslation = db.QueryWord(i).get('translation', '')  # 单词翻译
            wordTranslation = (' '.join(wordTranslation.split()))
            if len(wordTranslation) > 30:
                wordTranslation = wordTranslation[:30] + '...'
            wordTranslationLabel = QLabel(wordTranslation)
            wordTranslationLabel.setSizePolicy(qSize)

            hbox = QHBoxLayout()
            hbox.addWidget(wordTextLabel)
            hbox.addWidget(wordTranslationLabel)

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







