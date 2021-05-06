# 文件名称：Server.py
# 主要功能：C/S架构的客户端
# 最后修改时间: 2021/05/04 18:41
# ======================================================================

from socket import *
import json
import time



def ClientMain(dataType, data):
    """
    客户端向服务器端发送数据
    :param dataType: 数据类型
    :param data: 数据内容
    :return: 若发送成功则返回服务器端信息，失败则返回False
    """
    if not data or dataType == "":
        return "登录信息错误"
    HOST = '127.0.0.1'
    PORT = 21567
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    rev = ""
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    try:
        tcpCliSock.connect(ADDR)
    except:
        rev = "服务器连接失败"
    if rev == "":  # 连接成功
        data = {dataType: data}
        data = json.dumps(data)  # 转为json格式
        try:
            tcpCliSock.send(bytes(data, 'utf-8'))  # 编码发送数据
            rev = tcpCliSock.recv(BUFSIZ)  # 得到服务器端回传信息
        except:
            rev = "服务器繁忙，请稍后再试"
        rev = rev.decode('utf-8')
        if rev == "":
            rev = "网络异常"
    return rev


def ClientLogin(username, password):
    """
    客户端登录
    :param username: 用户名
    :param password: 密码
    :return: ClientMain的返回值
    """
    data = {"username": username, "password": password}
    dataType = "login"
    return ClientMain(dataType, data)


def ClientRegister(username, password):
    """
    客户端注册
    :param username: 用户名
    :param password: 密码
    :return: ClientMain的返回值
    """
    data = {"username": username, "password": password, "type": "client"}
    dataType = "register"
    return ClientMain(dataType, data)


def ClientFeedback(username, text):
    """
    客户端反馈
    :param username: 用户名
    :param text: 反馈内容
    :return: ClientMain的返回值
    """
    data = {"username": username, "text": text, "time": time.ctime()}
    dataType = "feedback"
    return ClientMain(dataType, data)


if __name__ == "__main__":
    # print(ClientLogin('user1', '123'))
    # print(ClientRegister('user1', '123456'))
    # print(ClientLogin('user1', '123456'))
    # print(ClientLogin('user1', '123'))
    # print(ClientRegister('user1', '123'))
    print(ClientFeedback('user1', '你好，我想反馈一些消息'))

