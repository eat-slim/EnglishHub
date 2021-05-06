# 文件名称：StudyEnglish.py
# 主要功能：学习英语的各项功能，包括背单词、单词测试
# 最后修改时间: 2021/04/02 19:47
# ======================================================================

import sqlite3
import time
import datetime
import random
import os

dbFile = 'ecdict.db'  # 词典数据库文件
reviewPlan = {"known": 1, "vague": 2, "unknown": 3}  # 复习计划，key:认识程度，value:基础复习天数
allCategoryWordsSum = {"zk": 0, "gk": 0, "cet4": 0, "cet6": 0, "ielts": 0, "toefl": 0}  # 记录所有类型单词总数

studyRecord = 'studyRecord.db'  # 学习记录
config = 'config.dat'  # 学习记录的配置文件


class StudyRecordDB:
    """学习记录的数据库读写"""

    def __init__(self, fileName, verbose=True):
        self.__dbName = fileName
        if fileName != ':memory:':
            os.path.abspath(fileName)
        self.__verbose = verbose
        self.__connection = None

        # 连接数据库
        self.__connection = sqlite3.connect(self.__dbName)
        # 建表
        self.__CreateDB()

    def __CreateDB(self):
        """创建数据库"""
        sql = '''
        CREATE TABLE IF NOT EXISTS "studyRecord" (
            "word" VARCHAR(64) NOT NULL UNIQUE,
            "isStudied" INTEGER DEFAULT(0),
            "tag" VARCHAR(16),
            "review" INTEGER DEFAULT(0),
            "reviewDate" REAL DEFAULT(0)
        );
        CREATE UNIQUE INDEX IF NOT EXISTS "studyRecord_word" ON studyRecord (word);
        '''

        # 去除sql文本内容每一行前面的缩进
        sql = '\n'.join([n.strip('\t') for n in sql.split('\n')])
        sql = sql.strip('\n')

        # 执行多行sql语句，并提交事务
        self.__connection.executescript(sql)
        self.__connection.commit()

    def __CloseDB(self):
        """关闭数据库"""
        if self.__connection:
            self.__connection.close()
        self.__connection = None

    def InsertNewWords(self, reciteList, commit=True):
        """将背诵单词列表插入学习记录数据库中"""
        sql0 = 'DELETE FROM studyRecord;'
        self.__connection.execute(sql0)
        sql = 'INSERT INTO studyRecord(word, isStudied, tag, review, reviewDate) VALUES(?, ?, ?, ?, ?);'
        for i in reciteList:
            try:
                self.__connection.execute(sql, (i.word, i.isStudied, i.tag, i.review, i.reviewDate))
            except sqlite3.IntegrityError as e:
                self.OutputLog(str(e))
                return False
            except sqlite3.Error as e:
                self.OutputLog(str(e))
                return False
        if commit:
            try:
                self.__connection.commit()
            except sqlite3.IntegrityError:
                return False
        return True

    def UpdateWord(self, word, commit=True):
        """更新背诵数据"""
        sql = 'UPDATE studyRecord SET isStudied=?, tag=?, review=?, reviewDate=? WHERE word =?'
        try:
            self.__connection.execute(sql, (word.isStudied, word.tag, word.review, word.reviewDate, word.word))
        except sqlite3.IntegrityError:
            return False
        if commit:
            try:
                self.__connection.commit()
            except sqlite3.IntegrityError:
                return False
        return True

    def GetAllWord(self):
        """取得所有单词"""
        return list(self.__iter__())

    def OutputLog(self, text):
        """输出日志"""
        if self.__verbose:
            print(text)
        return True

    def commit(self):
        """提交变更"""
        try:
            self.__connection.commit()
        except sqlite3.IntegrityError:
            self.__connection.rollback()
            return False
        return True

    def CountSum(self):
        """统计单词总数"""
        c = self.__connection.cursor()
        c.execute('select count(*) from studyRecord;')
        record = c.fetchone()
        return record[0]

    def DeleteAll(self):
        """清空数据库"""
        # 修改SQLite系统表数据
        sql1 = 'DELETE FROM studyRecord;'
        # sql2 = "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'studyRecord';"
        try:
            self.__connection.execute(sql1)
            # self.__connection.execute(sql2)
            self.__connection.commit()
        except sqlite3.IntegrityError as e:
            self.OutputLog(str(e))
            return False
        except sqlite3.Error as e:
            self.OutputLog(str(e))
            return False
        return True

    def __iter__(self):
        """浏览所有记录"""
        c = self.__connection.cursor()
        sql = 'select * from "studyRecord"'
        c.execute(sql)
        return c.__iter__()

    def __len__(self):
        """取得长度"""
        return self.CountSum()

    def __del__(self):
        self.__CloseDB()


class Word:
    """单词类，记录每个单词的学习信息"""

    def __init__(self, word, isStudied=False, tag="", review=0, reviewDate=0.0):
        self.word = word  # 单词文本
        self.isStudied = isStudied  # 是否被学习
        self.tag = tag  # 单词认识程度的标记，包括：熟悉"known"，模糊"vague"，不认识"unknown"
        self.review = review  # 记录单词剩余复习天数
        self.reviewDate = reviewDate  # 记录单词上一次复习时间

    def Study(self, tag="unknown"):
        """学习到此单词时调用该函数，设置部分学习信息
        tag:学习时选择的认识程度"""
        # 更新单词学习情况
        if not self.isStudied:
            self.tag = tag
            self.review = reviewPlan.get(self.tag, 3)
            self.isStudied = True
        return

    def Review(self, tag="unknown"):
        """复习到此单词时调用该函数，更新复习情况
        tag:复习时选择的认识程度，只有"unknown"和"known"两种情况"""
        # 复习时选择认识则复习天数减少1天，否则复习天数不变
        if self.review <= 0:
            pass
        elif tag == "known":
            self.review -= 1
        self.reviewDate = time.time()
        return

    def ReviewRemaining(self):
        """返回剩余复习天数"""
        return self.review

    def WordText(self):
        """返回单词文本"""
        return self.word

    def IsStudied(self):
        """返回是否学习"""
        return self.isStudied

    def ReadyToStudy(self):
        """返回是否为待学习"""
        return not self.isStudied


class ReciteWords:
    """背诵单词类，记录背诵信息"""

    def __init__(self, category="", dailyNumber=-1, sequence=0):
        """category是背诵类别，dailyNumber是背诵天数，这俩为默认值时代表数据已被写入配置文件"""
        self.category = category  # 背诵类别，包括中考、高考、CET4、CET6等
        self.dailyNumber = dailyNumber  # 每日单词背诵量
        self.sequence = sequence  # 背诵顺序，0为乱序，1为顺序
        self.wordsSum = allCategoryWordsSum.get(category, 0)  # 单词总量
        self.db = StudyRecordDB(studyRecord)  # 打开学习记录数据库
        self.startTime = time.time()  # 背诵开始时间
        self.remainingNumber = dailyNumber  # 记录当日剩余背诵单词数

        self.reciteList = self.CreateReciteList()  # 生成背诵单词列表
        self.Configure()  # 配置信息

    def Configure(self):
        """配置学习记录的基本信息"""
        if self.category == "":
            # 默认值，读配置文件
            with open(config, 'r') as configFile:
                configList = [i.strip() for i in configFile.readlines()]
            self.category = configList[0]
            self.dailyNumber = int(configList[1])
            self.sequence = int(configList[2])
            self.startTime = float(configList[3])
            self.remainingNumber = int(configList[4])
            self.wordsSum = allCategoryWordsSum.get(self.category, 0)  # 单词总量
        else:
            # 非默认值，为初次学习，写配置文件
            self.WriteConfig()

    def WriteConfig(self):
        """写配置文件"""
        with open(config, 'w+') as configFile:
            configFile.write(self.category + '\n')
            configFile.write(str(self.dailyNumber) + '\n')
            configFile.write(str(self.sequence) + '\n')
            configFile.write(str(self.startTime) + '\n')
            configFile.write(str(self.remainingNumber) + '\n')

    def CreateReciteList(self):
        """根据背诵类别生成背诵列表并排序或打乱"""
        if self.category == "":
            # 默认值，读数据库文件
            wordsTuple = self.db.GetAllWord()
            return [Word(i[0], i[1], i[2], i[3], i[4]) for i in wordsTuple]
        else:
            # 初次生成背诵单词，在数据库中查找此类别单词，创建背诵列表，排序或打乱后返回
            db = sqlite3.connect(dbFile)
            dbc = db.cursor()
            sql = "select word from dictionary where tag like ?"
            dbc.execute(sql, ('%' + self.category + '%',))
            execResult = dbc.fetchall()
            reciteList = [Word(i[0]) for i in execResult]
            if self.sequence == 0:
                random.shuffle(reciteList)
            elif self.sequence == 1:
                reciteList.sort(key=lambda word: word.word)
            self.db.InsertNewWords(reciteList)  # 写入数据库
            return reciteList

    def ShowReciteList(self):
        """展示背诵列表的单词"""
        for word in self.reciteList:
            print(word.WordText())
        print('length:', len(self.reciteList))

    def DailyRecite(self):
        """生成每日背诵单词"""
        # 从背诵列表中顺次抽取等同于每日剩余背诵单词数量的单词文本
        return [i[1].WordText() for i in zip(range(self.remainingNumber), filter(Word.ReadyToStudy, self.reciteList))]

    def ReciteWord(self, word, tag="unknown"):
        """背诵每个单词时调用此函数
        word:背诵的单词文本，tag:学习时选择的认识程度"""
        try:
            index = [i.word for i in self.reciteList].index(word)
            self.reciteList[index].Study(tag=tag)
            self.db.UpdateWord(self.reciteList[index])
            self.remainingNumber -= 1
            self.WriteConfig()
        except ValueError:
            return 'ValueError'
        except Exception:
            return 'Error'

    def CompareDate(self, cmpTime):
        """比较日期数据和今天日期是否相等"""
        thisDate = datetime.datetime.fromtimestamp(self.startTime)
        cmpDate = datetime.datetime.fromtimestamp(cmpTime)
        if thisDate.year == cmpDate.year and thisDate.month == cmpDate.month and thisDate.day == cmpDate.day:
            return True
        else:
            return False

    def DailyReview(self):
        """生成每日复习单词的列表"""
        return [i.word for i in self.reciteList if i.review and not self.CompareDate(i.reviewDate)]

    def ReviewWord(self, word, tag="unknown"):
        """复习单词时调用此函数
        word:复习的单词文本，tag:复习时选择的认识程度"""
        try:
            index = [i.word for i in self.reciteList].index(word)
            self.reciteList[index].Review(tag=tag)
            self.db.UpdateWord(word)
        except ValueError:
            return 'ValueError'
        except Exception:
            return 'Error'

    def RecitedWords(self):
        """返回已背诵单词的列表"""
        return [i.word for i in self.reciteList if i.isStudied]

    def ReadyToReviewWord(self):
        """返回待复习单词列表"""
        return [(i.word, i.review) for i in self.reciteList if i.review]

    def IsOver(self):
        """检测背诵计划是否完成"""
        for i in self.reciteList:
            if i.review or not i.isStudied:
                return False
        return True

    def Delete(self):
        """
        清除学习计划
        :return:
        """
        os.remove(studyRecord)
        os.remove(config)



def test1():
    """测试函数1，模拟单词背诵情况"""
    recite = ReciteWords('zk', 30, 0)  # 生成背诵计划对象，选择中考词汇，每日背诵30词，乱序背诵
    recite.ShowReciteList()  # 展示背诵计划包含单词的文本

    i = 1
    # 连续背诵
    while True:
        print('背诵天数：', i)
        i += 1
        reciteDay1 = recite.DailyRecite()  # 今日背诵单词
        reviewDay1 = recite.DailyReview()  # 今日复习单词
        print('今日背诵单词：', reciteDay1)
        print('今日复习单词：', reviewDay1)
        if len(reciteDay1):
            for word in reciteDay1:
                recite.ReciteWord(word, tag="unknown")  # 背诵所有单词，且都不认识
        if len(reviewDay1):
            for word in reviewDay1:
                recite.ReviewWord(word, tag="known")  # 复习所有单词，且都认识
        print('当前已背诵单词：', recite.RecitedWords())  # 展示已背诵单词
        print('当前待复习单词：', recite.ReadyToReviewWord())  # 展示待复习单词

        # 检测背诵计划是否完成
        if recite.IsOver():
            print("背诵计划完成~")
            break
        # os.system('pause')  # 按回车键继续
        time.sleep(5)  # 等待5秒继续


def test2():
    """测试函数2，测试学习记录数据库"""
    testList = ['hello', 'world', 'computer', 'science', 'and', 'technology']
    testList = [Word(i) for i in testList]
    record = StudyRecordDB(studyRecord)
    record.InsertNewWords(testList)
    print(record.GetAllWord())
    for i in testList:
        i.Study()
        record.UpdateWord(i)
    print(record.GetAllWord())


def test3():
    """数据库创建后的读写"""
    record = StudyRecordDB(studyRecord)
    readList = record.GetAllWord()
    wordsList = [Word(i[0], i[1], i[2], i[3]) for i in readList]
    for i in wordsList:
        print(i.WordText(), i.IsStudied(), i.tag, i.ReviewRemaining())


def test4():
    """
    完整测试
    :return:
    """
    recite = ReciteWords('zk', 30, 0)  # 生成背诵计划对象，选择中考词汇，每日背诵30词，乱序背诵
    recite.ShowReciteList()  # 展示背诵计划包含单词的文本
    l = recite.DailyRecite()
    print(l)

    day1 = ReciteWords()
    l2 = day1.ReciteWord()
    l = day1.DailyRecite()
    print(l[:15])
    for i in l[:15]:
        day1.ReciteWord(i, "known")

    day1_2 = ReciteWords()
    l = day1_2.DailyRecite()
    print(l)
    for i in l:
        day1_2.ReciteWord(i, "known")

    day1_3 = ReciteWords()
    l = day1_3.DailyRecite()
    print(l)
    for i in l:
        day1_3.ReciteWord(i, "known")

    l = day1_3.ReadyToReviewWord()
    print(l)


if __name__ == "__main__":
    # test1()
    # test2()
    # test3()
    test4()
    # r = ReciteWords()
    # r.Delete()
