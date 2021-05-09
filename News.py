# 文件名称：News.py
# 主要功能：每日新闻，给出新闻的标题和链接，以及每日新闻的界面
# ======================================================================

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
import urllib.request
import requests
import re
import os
import shutil
import sys


class SearchNewsUI(QWidget):
    """
    每日新闻的界面类
    """

    def __init__(self):
        super(SearchNewsUI, self).__init__()
        self.resize(1024,720)
        self.newsStrip = QListWidget()  # 新闻展示栏为列表
        self.vbox = QVBoxLayout()  # 垂直布局展示新闻
        self.vbox.addWidget(self.newsStrip)
        self.setLayout(self.vbox)
        self.CreateListItem()
        self.setStyleSheet('''
            QListWidget{
	            border: none;
	            background-color:#F5F5F5;
	            border-radius:10px;
	            
            }
            QListWidget::item{
                padding:10px;
                background-color:#F5F5F5;
                margin:10px;
                border-radius:20px;
            }
            QListWidget::item:hover{
                background-color:#D3D3D3;
                border-bottom:1px solid rgb(216,191,216);
                border-radius:20px;
            }
            QListWidget::item:selected
            {
                background-color:#C0C0C0;
                padding:0px;
                margin:0px;
                color:transparent;
                border-radius:20px;
            }
            QListWidget::item:selected:!active
            {
                border-width:0px;
                border-radius:20px;
            }

        ''')
    def CreateListItem(self):
        """
        根据新闻填充列表内容
        :return:
        """
        qSize = QSizePolicy()
        qSize.setHorizontalPolicy(QSizePolicy.Ignored)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        news = SearchNews()
        if "error" in news:
            label = QLabel('网络异常，获取新闻失败')
            label.setFont(font)
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item = QListWidgetItem()  # 列表项目
            item.setSizeHint(QSize(0, 200))
            style = QWidget()  # 项目样式
            vbox = QVBoxLayout()
            vbox.addWidget(label)
            style.setLayout(vbox)
            self.newsStrip.addItem(item)
            self.newsStrip.setItemWidget(item, style)
        else:
            for key in news.keys():
                item = QListWidgetItem()  # 列表项目
                item.setSizeHint(QSize(0, 200))
                style = QWidget()  # 项目样式
                img = QLabel()  # 新闻图片
                text = QLabel()  # 新闻标题
                # 导入图片
                img.setPixmap(QPixmap('Pic\\%s.png' % (re.sub(r'[| ]', '_', key[:20]),)))
                img.setScaledContents(True)
                img.setSizePolicy(qSize)
                # 标题作为外部链接
                title = key
                site = news[key]["site"]
                if len(title) > 100:
                    title = title[:100] + '...'
                text.setText("<a href=%s style='color:black'>%s</a>" % (site, title))
                text.setOpenExternalLinks(True)
                text.setWordWrap(True)
                text.setFont(font)
                # 项目采用水平布局
                hbox = QHBoxLayout()
                hbox.addWidget(img)
                hbox.addWidget(text)
                hbox.setStretch(0, 1)
                hbox.setStretch(1, 2)
                style.setLayout(hbox)  # 水平布局
                self.newsStrip.addItem(item)
                self.newsStrip.setItemWidget(item, style)
            shutil.rmtree('Pic')


def SearchNews(url='http://www.xinhuanet.com/english/home.htm'):
    """
    查询某一网站的新闻标题和链接
    :param url: 网站地址
    :return: 返回字典，其中key为新闻标题，value为由链接和图片组成的字典
    """
    news = {}
    # 解析网站源码
    try:
        web = urllib.request.urlopen(url)
        sourceData = web.read().decode()
        web.close()
    except Exception as e:
        news['error'] = "连接异常：" + str(e)
        return news

    # 使用正则表达式获取网站当日新闻的标签
    pattern = re.compile(r'<a href="http://www.xinhuanet.com/english/20.*" target="_blank"><img src=.*/></a>')
    patternTitle = re.compile(r'<a.*><img src=".*" alt="(.*)" /></a>')
    patternSite = re.compile(r'<a href="(.*)" target="_blank">')
    patternImg = re.compile(r'<a.*><img src="(.*)" alt=".*" /></a>')
    processData = pattern.findall(sourceData)
    processData = [i for i in processData if i is not None]

    # 对标签进行二次处理，提取标题以及对应的链接和图片，并填写到字典
    num = 0
    for i in processData:
        label = i
        title = patternTitle.findall(i)
        site = patternSite.findall(i)
        img = patternImg.findall(i)
        if len(title) > 0 and len(site) > 0 and len(img) > 0:
            title = title[0]
            site = site[0]
            img = img[0]
            info = {"site": site, "img": img, "label": label}
            r = requests.get(img)
            if not os.path.exists("Pic"):
                os.makedirs("Pic")
            with open('Pic\\' + re.sub(r'[| ]', '_', title[:20]) + '.png', 'wb') as f:
                f.write(r.content)
            news[title] = info
    return news


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = SearchNewsUI()
    main.show()
    sys.exit(app.exec_())

