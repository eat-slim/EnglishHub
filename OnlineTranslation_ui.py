# 文件名称：OnlineTranslation_ui.py
# 主要功能：在线翻译的界面
# 最后修改时间: 2021/04/07 23:00
# ======================================================================

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from OnlineTranslation import *
import sys


class OnlineTranslationUI(QWidget):
    """在线翻译模块的界面类"""

    def __init__(self):
        super(OnlineTranslationUI, self).__init__()
        self.resize(700, 500)

        self.inputText = QTextEdit()  # 多行输入框
        self.outputText = QTextEdit()  # 用多行输入框显示输出
        self.transButton = QPushButton("翻译")  # 翻译按钮

        self.FormatText()  # 设置文字格式

        layout = QVBoxLayout()  # 垂直布局
        layout.addWidget(self.inputText)
        layout.addWidget(self.transButton)
        layout.addWidget(self.outputText)

        self.setLayout(layout)

        self.transButton.clicked.connect(self.OnClickTransButton)  # 翻译按钮连接信号槽

    def OnClickTransButton(self):
        """点击查询按钮，进行翻译"""
        def ErrorCodeProcess(errorCode):
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
            msgBox = QMessageBox(QMessageBox.Warning, '警告', text)
            msgBox.exec_()

        # 获取输入信息，并调用翻译模块
        sourceText = self.inputText.toPlainText()
        res_dict = Translate(sourceText)

        # 异常处理
        if "error_code" in res_dict:
            ErrorCodeProcess(res_dict["error_code"])
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


def OnlineTranslation_uiTest():
    app = QApplication(sys.argv)
    ui = OnlineTranslationUI()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    OnlineTranslation_uiTest()
