# 文件名称：DataBase.py
# 主要功能：类封装词典数据库基本操作
# ======================================================================
import os
import sqlite3
import json


dictionaryDB = 'Data\\ecdict.db'  # 词典数据库文件
dictionaryLog = 'Log\\logDictionary.dat'


def StripWord(word):
    """将单词内容转化为小写，并只保留数字和字母部分"""
    return (''.join([n for n in word if n.isalnum()])).lower()


class DictionaryDB(object):
    """英汉字典数据库"""

    def __init__(self, fileName, verbose=True):
        self.__dbName = fileName
        if fileName != ':memory:':
            os.path.abspath(fileName)
        self.__connection = None
        self.__verbose = verbose

        # 连接数据库
        self.__connection = sqlite3.connect(self.__dbName)

        # 使用字典记录词典实体的各个属性
        fields = ('id', 'word', 'sw', 'phonetic', 'definition', 'translation', 'pos', 'collins', 'oxford',
                  'tag', 'bnc', 'frq', 'exchange', 'detail', 'audio')
        self.__fields = tuple([(fields[i], i) for i in range(len(fields))])
        self.__names = {}
        for k, v in self.__fields:
            self.__names[k] = v
        self.__enable = self.__fields[3:]

    def __CreateDB(self):
        """创建数据库,建立实体和索引"""
        sql = '''
        CREATE TABLE IF NOT EXISTS "dictionary" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            "word" VARCHAR(64) COLLATE NOCASE NOT NULL UNIQUE,
            "sw" VARCHAR(64) COLLATE NOCASE NOT NULL,
            "phonetic" VARCHAR(64),
            "definition" TEXT,
            "translation" TEXT,
            "pos" VARCHAR(16),
            "collins" INTEGER DEFAULT(0),
            "oxford" INTEGER DEFAULT(0),
            "tag" VARCHAR(64),
            "bnc" INTEGER DEFAULT(NULL),
            "frq" INTEGER DEFAULT(NULL),
            "exchange" TEXT,
            "detail" TEXT,
            "audio" TEXT
        );
        CREATE UNIQUE INDEX IF NOT EXISTS "dictionary_id" ON dictionary (id);
        CREATE UNIQUE INDEX IF NOT EXISTS "dictionary_word" ON dictionary (word);
        CREATE INDEX IF NOT EXISTS "dictionary_sw_wordcn" ON dictionary (sw, word collate nocase);
        CREATE INDEX IF NOT EXISTS "dictionary_wordcn" ON dictionary (word collate nocase);
        '''

        # 去除sql文本内容每一行前面的缩进
        sql = '\n'.join([n.strip('\t') for n in sql.split('\n')])
        sql = sql.strip('\n')

        # 执行多行sql语句，并提交事务
        self.__connection.executescript(sql)
        self.__connection.commit()

        return True

    def __RecordToDict(self, record):
        """数据库记录转化为字典"""
        if record is None:
            return None

        # 创建字典，并从__fields元组中取出字典的key，将record的内容作为value
        word = {}
        for k, v in self.__fields:
            word[k] = record[v]

        # detail内容为json格式下的字典形式保存例句，如果有例句则需要使用load得到内容
        if word['detail']:
            text = word['detail']
            try:
                obj = json.loads(text)
            except:
                obj = None
            word['detail'] = obj
        return word

    def __CloseDB(self):
        """关闭数据库"""
        if self.__connection:
            self.__connection.close()
        self.__connection = None

    def __del__(self):
        self.__CloseDB()

    def OutputLog(self, text):
        """输出日志"""
        if self.__verbose:
            if not os.path.exists("log"):
                os.makedirs("log")
            with open(dictionaryLog, 'a+') as f:  # 写入日志
                f.write(text)
                f.write('\n')
        return True

    def QueryWord(self, key):
        """查询单词"""
        c = self.__connection.cursor()

        # 判断查询类别是单词文本还是主码
        if isinstance(key, int) or isinstance(key, int):
            c.execute('select * from dictionary where id = ?;', (key,))
        elif isinstance(key, str) or isinstance(key, str):
            c.execute('select * from dictionary where word = ?', (key,))
        else:
            return None
        record = c.fetchone()

        # 数据库记录转化为字典形式
        return self.__RecordToDict(record)

    def QueryWordMatch(self, word, limit=10, strip=False):
        """单词匹配，匹配最相似的前limit个单词
        word:被匹配单词；limit:匹配单词数量；strip:是否采用模糊匹配，即不考虑字母大小写和非字母数字字符"""
        c = self.__connection.cursor()
        if not strip:
            sql = 'select id, word from dictionary where word >= ? '
            sql += 'order by word collate nocase limit ?;'
            c.execute(sql, (word, limit))
        else:
            sql = 'select id, word from dictionary where sw >= ? '
            sql += 'order by sw, word collate nocase limit ?;'
            c.execute(sql, (StripWord(word), limit))
        records = c.fetchall()
        result = []
        for record in records:
            result.append(tuple(record))
        return result

    def QueryBatch(self, keys):
        """批量查询
        keys:单词文本或键值的可迭代对象，如列表"""
        sql = 'select * from dictionary where '
        if keys is None:
            return None
        if not keys:
            return []

        # 使用列表保存每个查询对应的sql语句部分，最终使用or语句整合成一条sql语句并执行
        querys = []
        for key in keys:
            if isinstance(key, int):
                querys.append('id = ?')
            elif key is not None:
                querys.append('word = ?')
        sql = sql + ' or '.join(querys) + ';'
        c = self.__connection.cursor()
        c.execute(sql, tuple(keys))

        # 分类处理查询结果
        query_word = {}
        query_id = {}
        for row in c:
            obj = self.__RecordToDict(row)
            query_word[obj['word'].lower()] = obj
            query_id[obj['id']] = obj
        results = []
        for key in keys:
            if isinstance(key, int):
                results.append(query_id.get(key, None))
            elif key is not None:
                results.append(query_word.get(key.lower(), None))
            else:
                results.append(None)
        return tuple(results)

    def CountSum(self):
        """统计单词总数"""
        c = self.__connection.cursor()
        c.execute('select count(*) from dictionary;')
        record = c.fetchone()
        return record[0]

    def RegisterNewWord(self, word, items, commit=True):
        """注册新单词"""
        sql = 'INSERT INTO dictionary(word, sw) VALUES(?, ?);'
        try:
            self.__connection.execute(sql, (word, StripWord(word)))
        except sqlite3.IntegrityError as e:
            self.OutputLog(str(e))
            return False
        except sqlite3.Error as e:
            self.OutputLog(str(e))
            return False
        self.UpdateWord(word, items, commit)
        return True

    def RemoveWord(self, key, commit=True):
        """删除单词"""
        if isinstance(key, int):
            sql = 'DELETE FROM dictionary WHERE id=?;'
        else:
            sql = 'DELETE FROM dictionary WHERE word=?;'
        try:
            self.__connection.execute(sql, (key,))
            if commit:
                self.__connection.commit()
        except sqlite3.IntegrityError:
            return False
        return True

    def DeleteAll(self, reset_id=False):
        """清空数据库"""

        # 修改SQLite系统表数据
        sql1 = 'DELETE FROM dictionary;'
        sql2 = "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'dictionary';"
        try:
            self.__connection.execute(sql1)
            if reset_id:
                self.__connection.execute(sql2)
            self.__connection.commit()
        except sqlite3.IntegrityError as e:
            self.OutputLog(str(e))
            return False
        except sqlite3.Error as e:
            self.OutputLog(str(e))
            return False
        return True

    def UpdateWord(self, key, items, commit=True):
        """更新单词数据"""
        names = []
        values = []
        for name, id in self.__enable:
            if name in items:
                names.append(name)
                value = items[name]
                if name == 'detail':
                    if value is not None:
                        value = json.dumps(value, ensure_ascii=False)
                values.append(value)
        if len(names) == 0:
            if commit:
                try:
                    self.__connection.commit()
                except sqlite3.IntegrityError:
                    return False
            return False
        sql = 'UPDATE dictionary SET ' + ', '.join(['%s=?' % n for n in names])
        if isinstance(key, str):
            sql += ' WHERE word=?;'
        else:
            sql += ' WHERE id=?;'
        try:
            self.__connection.execute(sql, tuple(values + [key]))
            if commit:
                self.__connection.commit()
        except sqlite3.IntegrityError:
            return False
        return True

    def __iter__(self):
        """浏览词典"""
        c = self.__connection.cursor()
        sql = 'select "id", "word" from "dictionary"'
        sql += ' order by "word" collate nocase;'
        c.execute(sql)
        return c.__iter__()

    def __len__(self):
        """取得长度"""
        return self.CountSum()

    def __contains__(self, key):
        """检测存在"""
        return self.QueryWord(key) is not None

    def __getitem__(self, key):
        """查询单词"""
        return self.QueryWord(key)

    def commit(self):
        """提交变更"""
        try:
            self.__connection.commit()
        except sqlite3.IntegrityError:
            self.__connection.rollback()
            return False
        return True

    def GetAllWord(self):
        """取得所有单词"""
        return [n for _, n in self.__iter__()]





