# 文件名称：OnlineTranslation.py
# 主要功能：利用小牛翻译API实现在线文本英汉互译
# 最后修改时间: 2021/04/01 20:10
# ======================================================================

import json
import urllib
import urllib.parse
import urllib.request


def Translate(sourceText):
    """调用小牛翻译API实现文本的在线翻译
    text:待翻译文本"""

    if len(sourceText) == 0:
        # 输入为空
        return {'error_code': 'empty'}
    elif len(sourceText) > 1500:
        # 文本长度过长
        return {'error_code': 'too long'}

    # 小牛翻译API接口和文本
    # from:待翻译语言；to:目标语言；apikey:小牛翻译API的密钥；sourceText
    url = 'http://free.niutrans.com/NiuTransServer/translation?'
    data = {"from": 'zh', "to": 'en', "apikey": '85043d2db973a7af011efa9a30ec71e1', "src_text": sourceText}
    data_en = urllib.parse.urlencode(data)
    req = url + "&" + data_en

    # 向翻译接口发送请求
    try:
        res = urllib.request.urlopen(req)
        res = res.read()
        res_dict = json.loads(res)
    except:
        # 网络连接异常
        res_dict = {'error_code': 'network anomaly'}
    return res_dict


def OnlineTranslationTest():
    while(True):
        str = input("待翻译文本：")
        text = Translate(str)
        print(text)

# OnlineTranslationTest()



