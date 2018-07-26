import pymysql
import logging
from collections import deque

# 获取logger的实例
logger = logging.getLogger("myPymysql")
# 指定logger的输出格式
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# 文件日志，终端日志
file_handler = logging.FileHandler("myPymysql")
file_handler.setFormatter(formatter)

# 设置默认的级别
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

class DBHelper:
  def __init__(self, host="127.0.0.1", user='root', 
               pwd='********',db='testdb',port=3306,
               charset='utf-8'):
    self.host = host
    self.user = user
    self.port = port
    self.passwd = pwd
    self.db = db
    self.charset = charset
    self.conn = None
    self.cur = None

  def connectDataBase(self):
    """
    连接数据库
    """
    try:
      # self.conn = pymysql.connect(host=self.host, 
      #                             user=self.user,
      #                             password=self.passwd,
      #                             db=self.db,
      #                             port=self.port,
      #                             charset=self.charset)
      self.conn =pymysql.connect(host="127.0.0.1",
        user='root',password="********",db="testdb",charset="utf8")

    except:
      logger.error("connectDataBase Error")
      return False

    self.cur = self.conn.cursor()
    return True

# def createData(self):
#   """
#     创建数据库
#   """
#   #self.connectDataBase()
#   sql = "create database if not exists "+self.db
#   try:
#     self.cur.execute(sql)
#   except:
#     logger.error("create database Error")
#     return False
#   return True

  def execute(self, sql, params=None):
    """
    执行一般的sq语句
    """
    if self.connectDataBase() == False:
      return False

    try:
      if self.conn and self.cur:
        self.cur.execute(sql, params)
        self.conn.commit()
    except:
      logger.error("execute"+sql)
      logger.error("params",params)
      return False
    return True

  def fetchCount(self, sql, params=None):
    if self.connectDataBase() == False:
      return -1
    self.execute(sql, params)
    return self.cur.fetchone() # 返回操作数据库操作得到一条结果数据

  def myClose(self):
    if self.cur:
      self.cur.close()
    if self.conn:
      self.conn.close()
    return True


if __name__ == '__main__':
  dbhelper = DBHelper()
  print(dbhelper.fetchCount("SELECT count(*) FROM `testdb`.`maoyan`;")[0])
  print(dbhelper.fetchCount('SELECT count(*) FROM `testdb`.`maoyan` WHERE time like "%中国%";')[0])

  # print(dbhelper.connectDataBase())
  # #dbhelper.createData()
  # #dbhelper.myClose()

  # sql = "create table maoyan(title varchar(50),actor varchar(200),time  varchar(100));"
  # result = dbhelper.execute(sql, None)
  # if result == True:
  #   print("创建表成功")
  # else:
  #   print("创建表失败")
  # dbhelper.myClose()

  # id_data = "m3"
  # title_data = "英雄本色3"
  # actor_data = '周润发'
  # time_data = '2018-03-23'
  # sql = "INSERT INTO testdb.maoyan(id,title,actor,time) VALUES (%s,%s,%s,%s);"
  # params = (id_data, title_data, actor_data, time_data)
  # result = dbhelper.execute(sql, params)
  # if result == True:
  #   print("插入成功")
  # else:
  #   print("插入失败")

  logger.removeHandler(file_handler)

