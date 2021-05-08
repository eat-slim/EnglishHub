# 文件名称：FavoriteWords.py
# 主要功能：收藏英语单词
# ======================================================================

import os


saveFilePath = 'Data\\Favorites.dat'


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



