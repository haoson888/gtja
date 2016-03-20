#encoding: utf-8  
import sqlite3,os,sys
#import time
  
#createtabsql1 = "create table if not exists scriptdata(id integer primary key autoincrement, name varchar(128), info varchar(128))"  
class DBDriver:  
  ''''' 
  The DBDriver class use to write the script data that parse from Excel file 
  '''  
      
  def __init__(self, dbfile, tabledesc):  
    self.tablename = tabledesc[0]  
    self.tablefield = tabledesc[1]  
    self.dbfile = os.path.split(os.path.realpath(__file__))[0] + dbfile
    self.conn = sqlite3.connect(self.dbfile)
  
  def cerateDB(self):  
    createlist = ["create table if not exists ", self.tablename, "(id integer primary key autoincrement, ", self.tablefield, ")"]  
    createsql = "".join(createlist)
    print self.dbfile
    self.conn = sqlite3.connect(self.dbfile)  
    self.conn.isolation_level = None   
    #self.conn.execute("drop table if exists " + self.tablename)  ###delete the eixst table  
    self.conn.execute(createsql)  ####create new table  
    #conn.execute("delete from " + tablename) ####delete all the recoreds  
    return   
    
  def execDB(self, execsql):    
    self.conn.execute(execsql)  
    self.conn.commit()  
    return  
  
  def getResult(self, selectsql):  
    self.cur = self.conn.cursor()  
    self.cur.execute(selectsql)  
    self.res = self.cur.fetchall()  
    return self.res  
      
  def getCount(self):  
    return len(self.res)  

  # def updateDB(self,selectsql):
  #   self.cur = self.conn.cursor()
  #   self.cur..execute('UPDATE book SET price=? WHERE id=?',(1000, 1))


  def closeDB(self):  
    self.cur.close()  
    self.conn.close()


  
''''' 
The example for using the DBDriver class 
'''  
if __name__ == '__main__':
  dbfile = "/aaa.db"


  tabledesc = ("scriptdata", "name varchar(128), info varchar(128)")
  insertsql = "insert into scriptdata(name,info) values ('test', 'only a test')"
  selectsql = "select * from scriptdata"

  dbd = DBDriver(dbfile, tabledesc)
  dbd.cerateDB()  
  dbd.execDB(insertsql)
  res = dbd.getResult(selectsql)
  rows = dbd.getCount()
  dbd.closeDB()

  print 'row:', rows
  for line in res:
    for col in line:
      print col