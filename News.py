# 文件名称：News.py
# 主要功能：新闻速递，给出新闻的标题和链接
# ======================================================================

import urllib.request
import re


def SearchNews(url='http://www.xinhuanet.com/english/home.htm'):
    """
    查询某一网站的新闻标题和链接
    :param url: 网站地址
    :return: 返回字典，其中key为新闻标题，value为标题对应的连接
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
    pattern = re.compile(r'<a href="http://www.xinhuanet.com/english/20.*" target="_blank">[^<=]*</a>')
    patternTitle = re.compile(r'<a.*>(.*)</a>')
    patternSite = re.compile(r'<a href="(.*)" target="_blank">')
    processData = pattern.findall(sourceData)
    processData = [i for i in processData if i is not None]

    # 对标签进行二次处理，提取标题和链接，并填写到字典
    for i in processData:
        title = patternTitle.findall(i)
        site = patternSite.findall(i)
        if len(title) > 0 and len(site):
            title = title[0]
            site = site[0]
        news[title] = site
    return news


print(SearchNews())

