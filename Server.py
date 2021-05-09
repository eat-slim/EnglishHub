# 文件名称：Server.py
# 主要功能：C/S架构的服务器端
# 最后修改时间: 2021/05/04 18:27
# ======================================================================

from socket import *
import json
import time
import os
import sqlite3
import _thread

userInformation = 'Data\\userInformation.db'


class ServerSide:
    """
    客户端
    """

    def __init__(self):
        self.HOST = ''
        self.PORT = 21567
        self.BUFSIZ = 4096
        self.ADDR = (self.HOST, self.PORT)

        self.tcpSvrSock = socket(AF_INET, SOCK_STREAM)
        self.tcpSvrSock.bind(self.ADDR)
        self.tcpSvrSock.listen(5)

        self.logServer = 'log\\server.dat'
        self.logFeedback = 'log\\feedback.dat'
        if not os.path.exists("log"):
            os.makedirs("log")
        if not os.path.exists('Data'):
            os.makedirs('Data')

    def ServerMain(self):
        """
        服务器端的主服务程序，接收客户端的TCP请求
        :return: 无返回
        """
        while True:
            print("Waiting for connection...")
            tcpCliSock, addr = self.tcpSvrSock.accept()  # 等待TCP连接
            print("...connected from", addr)
            data = tcpCliSock.recv(self.BUFSIZ)  # 接收数据
            if not data:
                continue
            try:
                # 创建新线程处理TCP服务，使TCP响应可以并行执行
                _thread.start_new_thread(self.ServerProcess, (tcpCliSock, addr, data))
            except:
                print("线程创建失败")
                if not os.path.exists("log"):
                    os.makedirs("log")
                with open(self.logServer, 'a+') as f:  # 写入日志
                    f.write("[%s] %s : 线程创建失败" % (time.ctime(), addr))
                    f.write('\n')
                continue

    def ServerProcess(self, tcpCliSock, addr, data):
        """
        TCP服务处理，对接受的数据分类进入对应的处理方法
        :param tcpCliSock: 用户TCP
        :param addr: 用户地址
        :param data: 数据
        :return: 无
        """
        data = json.loads(data.decode('utf-8'))  # 解码数据
        log = "[%s] %s : %s" % (time.ctime(), addr, data)
        self.ServerLog(log, self.logServer)
        print(log)
        returnMsg = ''
        if "login" in data:
            returnMsg = self.ServerLogin(data.get("login", ''))
        elif "register" in data:
            returnMsg = self.ServerRegister(data.get("register", ''))
        elif "feedback" in data:
            returnMsg = self.ServerFeedback(data.get("feedback", ''))
        tcpCliSock.send(bytes(returnMsg, 'utf-8'))  # 返回客户端信息
        tcpCliSock.close()  # 关闭连接

    def ServerLogin(self, dic):
        """
        用户登录接口
        :param dic: 登录信息
        :return: 登录成功返回"登录成功"，否则返回提示信息
        """
        username = dic.get("username", '')
        password = dic.get("password", '')
        if username == '' or password == '':
            return "登录异常"
        if not os.path.exists('Data'):
            os.makedirs('Data')
        db = UserInformationDB(userInformation)
        if db.QueryPassword(username) == password:
            return "登录成功"
        else:
            return "用户名或密码错误"

    def ServerRegister(self, dic):
        """
        用户注册接口
        :param dic: 注册信息
        :return: 注册成功返回"注册成功"，否则返回提示信息
        """
        username = dic.get("username", '')
        password = dic.get("password", '')
        type = dic.get("type", '')
        if username == '' or password == '' or type == '':
            return "注册异常"
        if not os.path.exists('Data'):
            os.makedirs('Data')
        db = UserInformationDB(userInformation)
        if db.Add(username=username, password=password, type=type):
            return "注册成功"
        else:
            return "注册失败，用户名重复"

    def ServerFeedback(self, dic):
        """
        用户反馈接口
        :param dic: 反馈信息
        :return: 成功接收返回“发送成功”，否则返回“发送失败”
        """
        username = dic.get("username", '')
        text = dic.get("text", '')
        ctime = dic.get("time", '')
        if username != '' and text != '' and ctime != '':
            log = "[%s] %s : %s" % (ctime, username, text)
            self.ServerLog(log, self.logFeedback)
            rcv = "发送成功"
        else:
            rcv = "发送失败"
        return rcv

    def ServerLog(self, log, file):
        """
        写入服务日志
        :param log: 日志内容
        :param file: 日志文件
        :return:
        """
        if not os.path.exists("log"):
            os.makedirs("log")
        with open(file, 'a+') as f:  # 写入文件
            f.write(log)
            f.write('\n')


class UserInformationDB:
    """
    用户信息数据库
    """

    def __init__(self, fileName, verbose=True):
        self.logDB = 'log\\serverDBLog.dat'
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
        """
        创建数据库
        :return:
        """

        sql = '''
        CREATE TABLE IF NOT EXISTS "userInformation" (
            "username" VARCHAR(16) NOT NULL UNIQUE,
            "password" VARCHAR(40),
            "type" VARCHAR(16),
            "register_time" REAL
        );
        CREATE UNIQUE INDEX IF NOT EXISTS "userInformation_username" ON userInformation (username);
        '''

        # 去除sql文本内容每一行前面的缩进
        sql = '\n'.join([n.strip('\t') for n in sql.split('\n')])
        sql = sql.strip('\n')

        # 执行多行sql语句，并提交事务
        self.__connection.executescript(sql)
        self.__connection.commit()

    def QueryPassword(self, username):
        """
        查找用户密码
        :param username: 用户名
        :return: 查找成功时返回用户密码，否则返回False
        """
        c = self.__connection.cursor()
        sql = 'select password from userInformation where username = ?'
        c.execute(sql, (username,))
        self.__connection.commit()
        record = c.fetchone()
        if record:
            return record[0]
        else:
            return False

    def QueryType(self, username):
        """
        查找用户类型
        :param username: 用户名
        :return: 查找成功时返回用户类型，否则返回False
        """
        c = self.__connection.cursor()
        sql = 'select type from userInformation where username = ?'
        c.execute(sql, (username,))
        self.__connection.commit()
        record = c.fetchone()
        if record:
            return record[0]
        else:
            return False

    def QueryUser(self, username):
        """
        查找用户详细信息
        :param username: 用户名
        :return: 查找成功时返回用户所有信息，否则返回False
        """
        c = self.__connection.cursor()
        sql = 'select * from userInformation where username = ?'
        c.execute(sql, (username,))
        self.__connection.commit()
        record = c.fetchone()
        if record:
            return list(record)
        else:
            return False

    def Add(self, username, password, type):
        """
        增添用户信息
        :param username: 用户名
        :param password: 密码
        :param type: 用户类型
        :return: 成功返回True，失败返回False
        """
        registerTime = time.time()
        sql = 'INSERT INTO userInformation(username, password, type, register_time) VALUES(?, ?, ?, ?);'
        try:
            self.__connection.execute(sql, (username, password, type, registerTime))
        except sqlite3.IntegrityError as e:
            self.OutputLog(str(e))
            return False
        except sqlite3.Error as e:
            self.OutputLog(str(e))
            return False
        try:
            self.__connection.commit()
        except sqlite3.IntegrityError:
            return False
        return True

    def Upgrade(self, username, password, type, oldUsername):
        """
        更新用户信息
        :param username: 新用户名
        :param password: 密码
        :param type: 用户类型
        :param oldUsername: 旧用户名
        :return: 成功返回True，失败返回False
        """
        if not self.QueryUser(username):
            sql = 'UPDATE userInformation SET username=?, password=?, type=? WHERE username =?;'
            try:
                self.__connection.execute(sql, (username, password, type, oldUsername))
            except sqlite3.IntegrityError as e:
                self.OutputLog(str(e))
                return False
            except sqlite3.Error as e:
                self.OutputLog(str(e))
                return False
            try:
                self.__connection.commit()
            except sqlite3.IntegrityError:
                return False
            return True
        else:
            return False

    def Delete(self, username):
        """
        注销用户
        :param username:
        :return: 注销成功返回True，否则返回False
        """
        sql = 'DELETE FROM userInformation WHERE username=?;'
        try:
            self.__connection.execute(sql, (username,))
            self.__connection.commit()
        except sqlite3.IntegrityError:
            return False
        return True

    def OutputLog(self, text):
        """输出日志"""
        if self.__verbose:
            if not os.path.exists("log"):
                os.makedirs("log")
            with open(self.logDB, 'a+') as f:
                f.write("[%s] %s" % (time.ctime(), text))
                f.write('\n')
        return True


if __name__ == "__main__":
    server = ServerSide()
    server.ServerMain()



