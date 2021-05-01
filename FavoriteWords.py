# 文件名称：FavoriteWords.py
# 主要功能：收藏英语单词
# 最后修改时间: 2021/04/25 18:28
# ======================================================================

import os


saveFilePath = 'Favorites.dat'


class Favorites:
    """收藏类"""
    def __init__(self):
        self.wordsList = ""
        if os.path.exists(saveFilePath):
            with open(saveFilePath, 'r') as self.saveFile:
                self.wordsList = [i.strip() for i in self.saveFile.readlines() if i.strip() != '']
        else:
            open(saveFilePath, 'w')

    def Add(self, word):
        """向收藏类链表中添加字符串表示的单词"""
        if word not in self.wordsList:
            # self.wordsList.append(word)
            self.wordsList.insert(0, word)
            with open(saveFilePath, 'w+') as self.saveFile:
                for i in self.wordsList:
                    self.saveFile.write(i)
                    self.saveFile.write('\n')

    def Delete(self, word):
        """将收藏夹中的单词删除"""
        if word in self.wordsList:
            self.wordsList.remove(word)
            with open(saveFilePath, 'w+') as self.saveFile:
                self.saveFile.truncate()
                for i in self.wordsList:
                    self.saveFile.write(i)
                    self.saveFile.write('\n')

    def DeleteAll(self):
        """将收藏夹中的单词全部删除"""
        self.wordsList.clear()
        with open(saveFilePath, 'w+') as self.saveFile:
            self.saveFile.truncate()

    def Show(self):
        """展示收藏夹的单词列表"""
        return self.wordsList

    def IsExist(self, word):
        """判断是否在收藏夹中"""
        return word in self.wordsList


def test():
    """测试程序"""
    c = Favorites()
    words = ['a', 'b', 'string']
    for i in words:
        c.Add(i)  # 增添
    print(c.Show(), c.IsExist('a'))
    c.Delete('a')
    c.Delete('unknown')
    print(c.Show(), c.IsExist('a'), c.IsExist('unknown'))

def test2():
    c = Favorites()
    c.Delete('b')
    print(c.Show())


if __name__ == "__main__":
    test2()
    # test2()



