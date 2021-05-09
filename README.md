# EnglishHub
## 一款桌面级的英语学习软件、工具
### 欢迎使用EnglishHub
> 我们是由五名计算机专业本科生组成的小组  
> 这是我们一起完成的英文学习软件 
> > 这是我们第一次尝试编写一款集成度较高且具有一定实用型的软件  
> > 虽然它现在还不是一个完美的产品  
> > 但之后，我们会不断地去完善它，希望它最终有一个完整的ending   
### 他现在的功能有  
+ 基于小牛翻译API的：在线翻译
+ 基于开源英汉词典的：单词查询
+ 依赖SQLite3数据库的：每日背单词、单词收藏
+ 基于HTTP请求的：每日新闻
+ 使用C/S架构、TCP协议+多线程的网络通信：注册、登录以及反馈
## 内容简介
### 编写环境
项目使用Python编写，并基于PyQt5制作了GUI</br>
Python版本为3.8.0
### 项目分支
+ Logic分支内为各个功能模块的底层代码
+ UI分支内为各个功能和主界面的界面代码
+ DictionaryDateBase分支内为我们使用的开源英汉词典数据库
## 使用方式
+ 下载所有的py文件和数据库文件
+ py文件同目录下建立名为"Data"的文件夹，将词典数据库放入Data文件夹中
+ 运行EnglishHub.py即可
### 补充
+ 程序图标可以放置在同目录下的Label文件夹内并命名为label.png
+ 所有运行日志都在同目录下的log文件夹内
+ 用户反馈记录的文件路径为log\\feedback.dat
## 更新日志
