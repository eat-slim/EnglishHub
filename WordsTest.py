# 文件名称：WordsTest.py
# 主要功能：实现单词测试功能
# 最后修改时间: 2021/04/27 16:19
# ======================================================================


import pyttsx3
from StudyEnglish import *


class WordsForTest:
    """单词测试类"""

    def __init__(self, testType='study', num=30):
        """
        testType：测试类型，默认值study代表测试学习计划中已学的单词，其他选项包括zk,gk,cet4,cet6,ielts,toefl
        num：单词测试数量，默认为30个，最多200个
        """
        self.testType = testType
        if num > 200:
            num = 200
        self.num = num
        self.rightNum = 0  # 测试通过的单词数量
        self.testList = self.CreatTestList()

    def CreatTestList(self):
        """
        生成测试单词列表
        :return: 成员为单词文本字符串的list
        """
        if self.testType == 'study':
            db = StudyRecordDB(studyRecord)
            testList = db.GetAllWord()
            testList = [i[0] for i in testList if i[1]][:self.num]  # 取出所有已学习的单词
        else:
            # 在数据库中查找此类别单词，创建测试列表
            db = sqlite3.connect(dbFile)
            dbc = db.cursor()
            sql = "select word from dictionary where tag like ?"
            dbc.execute(sql, ('%' + self.testType + '%',))
            execResult = dbc.fetchall()
            testList = [i[0] for i in execResult]
            random.shuffle(testList)
            testList = testList[:self.num]
        print(testList)
        return testList

    def Dictation(self, index):
        """
        听写单词
        :param index:听写单词的进度
        :return: 听写完成：空字符串，否则：待听写的单词文本
        """
        maxIndex = min(self.num, len(self.testList))
        if 0 <= index < maxIndex:
            word = self.testList[index]
            PronunceWord(word)
            return word
        else:
            return ""

    def TestNum(self):
        """
        返回测试单词的总数
        """
        return self.num


def PronunceWord(word):
    """
    发音函数
    以字符串形式传入，输出音频
    输入的字符串可以是包含多个单词的句子，那么就会朗读出句子
    """
    engine = pyttsx3.Engine()
    engine.setProperty('rate', 150)  # 设置听写语速， 默认为200
    engine.setProperty('volume', 2.0)  # 设置音量， 默认为1.0
    engine.say(word)
    engine.runAndWait()


def WordsTest_Test():
    test = WordsForTest(testType='study')
    for i in range(test.TestNum()):
        word = test.Dictation(i)
        print(word)
        time.sleep(3)


if __name__ == "__main__":
    # engine = pyttsx3.Engine()
    # engine.say('hello')
    # engine.say('world')
    # engine.runAndWait()
    # rate = engine.getProperty('rate')
    # print(rate)
    # volume = engine.getProperty('volume')
    # print(volume)
    WordsTest_Test()
