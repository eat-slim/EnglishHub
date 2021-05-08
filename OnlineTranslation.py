# 文件名称：OnlineTranslation.py
# 主要功能：利用小牛翻译API实现在线文本英汉互译
# ======================================================================

import json
import urllib
import urllib.parse
import urllib.request


def Translate(sourceText, transType=0):
    """
    调用小牛翻译API实现文本的在线翻译
    :param sourceText: 待翻译文本
    :param transType: 翻译类型
    :return: 翻译结果
    """

    if len(sourceText) == 0:
        # 输入为空
        return {'error_code': 'empty'}
    elif len(sourceText) > 1500:
        # 文本长度过长
        return {'error_code': 'too long'}

    # 小牛翻译API接口和文本
    # from:待翻译语言；to:目标语言；apikey:小牛翻译API的密钥；sourceText
    url = 'http://free.niutrans.com/NiuTransServer/translation?'
    if transType == 0:
        data = {"from": 'zh', "to": 'en', "apikey": '85043d2db973a7af011efa9a30ec71e1', "src_text": sourceText}
    else:
        data = {"from": 'en', "to": 'zh', "apikey": '85043d2db973a7af011efa9a30ec71e1', "src_text": sourceText}
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



