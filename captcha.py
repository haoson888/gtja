#coding: utf-8
#date: 2015/12/28
#author: lylh

import cookielib
import urllib2
import urllib
import socket
import sys,os
import datetime
import time
import random
import re
import base64
import thread
import pytesseract
from PIL import Image
import requests
from StringIO import StringIO
from bs4 import BeautifulSoup
import smtplib
import ConfigParser
from email.mime.text import MIMEText
import getStockMsg

# proxies = {'http': 'http://192.168.199.214:8888',
#                    'https': '192.168.199.214:8888'}
proxies = {'http': 'http:://100.84.92.213:8889',
                   'https': '100.84.92.213:8889'}
headers = {"Host": "trade.gtja.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Origin": "https://trade.gtja.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4"}

liteheaders = {'Host': 'trade.gtja.com',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Connection': 'keep-alive',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
'Accept-Language': 'zh-cn',
'Accept-Encoding': 'gzip, deflat'}


#获取config配置文件
def getConfig(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/config.ini'
    config.read(path)
    return config.get(section, key)


def send_mail(to_list,sub,content):
    mail_host="smtp.126.com"
    mail_user=getConfig("MAIL_DATA_SOURCE_INFO","username")
    mail_pass=getConfig("MAIL_DATA_SOURCE_INFO","password")
    mail_postfix="126.com"
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False

#获取脚本文件的当前路径
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

cookiesPath = cur_file_dir() + "/cookies";
def readCookies():
    openCookiefile= open(cookiesPath,"r")
    cookies = openCookiefile.read()
    return cookies


def parserBodyData(data):
  newdata = {}
  for line in data.split("\n"):
       key = line.split(":")
       newdata[key[0]] = key[1]
  return newdata


def getCaptchaCode(headers,cookies):
  headers['Cookie'] = cookies
  catp_url = 'https://trade.gtja.com/webtrade/commons/verifyCodeImage.jsp'
  imagefile = requests.get(catp_url,headers=headers)
  image = Image.open(StringIO(imagefile.content))
  # f = open('/Users/lylh/Desktop/capta.jpg','wb')
  # f.write(imagefile.content)
  # f.close()
  vcode = pytesseract.image_to_string(image)
  # print vcode
  return vcode


def getCookies(cookiesPath):
  url = "https://trade.gtja.com/webtrade/trade/webTradeAction.do?method=preLogin"
  headers = '''Host: trade.gtja.com
Accept-Encoding: gzip, deflate
Cookie: __v3_c_last_10891=1451205662321; __v3_c_pv_10891=1; __v3_c_review_10891=0; __v3_c_session_10891=1451205662321814; __v3_c_session_at_10891=1451205710520; __v3_c_sesslist_10891=eaeqoebr86_cyk; __v3_c_today_10891=1; __v3_c_visitor=1451205662321814; Hm_lpvt_1c5bee4075446b613f382dd399824571=1451205663; Hm_lvt_1c5bee4075446b613f382dd399824571=1451205663
Connection: keep-alive
Proxy-Connection: keep-alive
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9
Accept-Language: zh-cn
Referer: http://www.gtja.com/i/
DNT: 1 '''
  newheaders = parserBodyData(headers)
  r = requests.get(url,headers=newheaders)
  cookies = r.cookies
  _cookies = ('; '.join(['='.join(item) for item in cookies.items()]))
  _MyBranchCodeList=4402
  _BranchName = '%u5E7F%u5DDE%u9EC4%u57D4%u5927%u9053%u8BC1%u5238%u8425%u4E1A%u90E8'
  _countType = 'Z'
  newcookies = 'BranchName='+_BranchName +';countType='+str(_countType)+';MyBranchCodeList='+str(_MyBranchCodeList)+';'+str(_cookies)
  print "cookies:"+newcookies

  f = open(cookiesPath,'w+')
  f.write(newcookies)
  f.close()
  return newcookies




def login(cookies,cookiesPath):
    url = "https://trade.gtja.com/webtrade/trade/webTradeAction.do"
    headers = {
    "Host": "trade.gtja.com",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Origin": "https://trade.gtja.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer":" https://trade.gtja.com/webtrade/trade/webTradeAction.do?method=preLogin",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
  }

    AppendCode = getCaptchaCode(headers,cookies)
    # print AppendCode
    # AppendCode = raw_input("captcheCode:")
    user = getConfig("GTJA_DATA_SOURCE_INFO","username")
    pwd = getConfig("GTJA_DATA_SOURCE_INFO","password")
    trdpwd = base64.b64encode(pwd);
    data = '''method:login
uid:'''+pwd+'''
pwdtype:
hardInfo:
logintype:common
flowno:
usbkeySn:
usbkeyData:
mac:
gtja_dating_login_type:0
availHeight:585
YYBFW:10
BranchCode:4402
BranchName:广州黄埔大道证券营业部
Page:
selectBranchCode:7001
countType:Z
inputid:'''+user+'''
trdpwd:'''+trdpwd+'''
AppendCode:''' + str(AppendCode)

    newdata = parserBodyData(data)
    # proxies = {"http:":"192.168.199.214:8888"}
    content = requests.post(url,data=newdata,headers=headers)

    loginHtml =  content.text
    soup = BeautifulSoup(loginHtml)
    
    if type(soup.title) != None:
      title =  soup.title.string
      print title
      #判断是否登录成功
      if title != "国泰君安证券欢迎您" :
          cookies = getCookies(cookiesPath)
          #重试登录
          login(cookies,cookiesPath)
      else:
          mailto_list=['328538688@qq.com']
          send_mail(mailto_list,"登录成功",title)

def getMenu(cookies):
  url = "https://trade.gtja.com/webtrade/trade/top.jsp?menu=stock"
  headers = '''Host: trade.gtja.com
Accept-Encoding: gzip, deflate
Connection: keep-alive
Proxy-Connection: keep-alive
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9
Accept-Language: zh-cn
DNT: 1'''

  newheaders = parserBodyData(headers)

  newheaders['Cookie']= cookies
  newheaders['Referer'] = "https://trade.gtja.com/webtrade/trade/webTradeAction.do"

  r = requests.get(url,headers=newheaders)
  # print r.content


def paperBuyjsp(headers,cookies,liteheaders,stkcode):
  url = "https://trade.gtja.com/webtrade/trade/webTradeAction.do"
  headers['Referer'] = "https://trade.gtja.com/webtrade/trade/PaperBuy.jsp"
  headers['Cookie'] = cookies
  data = {
    'method':'changekEntrust',
    'optype':'buy',
    'stkcode':stkcode,
    '_':''
  }

  getHqUrl = "https://trade.gtja.com/webtrade/trade/webTradeAction.do?method=getHq&stkcode="+str(stkcode)+"&bsflag=B"
  r = requests.post(url,data=data,headers=headers)

  liteheaders['Referer'] = "https://trade.gtja.com/webtrade/trade/PaperBuy.jsp"
  liteheaders['Cookie'] = cookies
  con = requests.get(getHqUrl,headers=liteheaders)
  return con.content

def niugwHeaders():
    data = '''Host: www.niuguwang.com
User-Agent: 牛股王 2.3.1 (iPhone; iPhone OS 9.0.2; zh_CN)
Connection: keep-alive
Accept-Encoding: gzip
Ver: ios_2.3.1
Connection: keep-alive
Uuid: c3572baa250d96570c01b2f6fdb06b633dfcc461'''
    headers= parserBodyData(data)
    return headers

def gethardeneAPI(stkcode):
      url = "http://www.niuguwang.com/tr/201411/getstock.ashx?version=2.3.1&packtype=0&s=App%20Store&usertoken=jQagMY41cB1ez7WqyhkszhMBXG2aGu2Iq-yMbevPecU*&stockcode="+str(stkcode)+"&contest=1"
      headers = niugwHeaders()
      r = requests.get(url=url,headers=headers)
      jsonData = r.json()
      # print jsonData
      rasingLimit = jsonData["rasingLimit"]
      limitDown=jsonData["limitDown"]
      maxBuy =jsonData["maxBuy"]
      innercode = jsonData["innercode"]
      maxSell = jsonData["maxSell"]
      lastAssets = jsonData["lastAssets"]
      return limitDown,rasingLimit,maxBuy,innercode,maxSell,lastAssets


def getPriceLimit(html):
  soup = BeautifulSoup(html)
  flag = 0
  for string in soup.stripped_strings:
      # print string
      if flag == 1:
          return string
          flag = 0
      elif string == u"跌停价：":
          flag =1

def gethardene(html):
  soup = BeautifulSoup(html)
  flag = 0
  for string in soup.stripped_strings:
      # print string
      if flag == 1:
          return string
          flag = 0
      elif string == u"涨停价：":
          flag =1

#判断是否买入还是卖出
def getRadioButton(followersMessageType):
    if followersMessageType == 1:
        radiobutton ="B"
    elif followersMessageType == 2:
        radiobutton ="S"
    else:
        radiobutton = 0
    return radiobutton

def simStockBuy(followersMessageType,hardene,PriceLimit,maxBuy,maxSell,innercode,lastAssets):
    radiobutton =getRadioButton(followersMessageType)

    if radiobutton == "B":
        price = float(hardene)- 0.01
        type = 1
        #计算买入股票数
        amount = (int(float(lastAssets)/float(price))/100)*100
    else:
        price = float(PriceLimit)+ 0.01
        #计算卖出股票数
        amount = maxSell
        type = 2
    headers = niugwHeaders()
    url = "http://www.niuguwang.com/tr/delegateadd.ashx?version=2.3.1&packtype=0&s=App%20Store&usertoken=jQagMY41cB1ez7WqyhkszhMBXG2aGu2Iq-yMbevPecU*&innercode="+str(innercode)+"&contest=1&price="+str(price)+"&amount="+str(amount)+"&type="+str(type)+"&share=0&buy=(null)"
    r = requests.get(url,headers)
    jsonData = r.json()
    print "simStockBuyjsonData:" +str(jsonData).decode('unicode_escape')

def PaperBuy(hardene,PriceLimit,headers,cookies,stkcode,followersMessageType):
    starttime = time.time()
    randomTime =  random.randint(000, 999)
    unixTime = int(time.mktime(datetime.datetime.now().timetuple()))
    gtja_entrust_sno =  str(unixTime) + str(randomTime)
    url = "https://trade.gtja.com/webtrade/trade/webTradeAction.do?method=entrustBusinessOut"
    headers['Cookie']= cookies
    headers['Referer'] = "https://trade.gtja.com/webtrade/trade/PaperBuy.jsp"
    radiobutton =getRadioButton(followersMessageType)

    if radiobutton == "B":
        price = hardene
    else:
        price = PriceLimit
    data='''gtja_entrust_sno:'''+gtja_entrust_sno+'''
stklevel:N
tzdate:0
market:2
stkcode:'''+stkcode+'''
radiobutton:'''+radiobutton+'''
price:'''+price+'''
qty:100'''
    newdata =parserBodyData(data)

    # print newdata
    r= requests.post(url,headers=headers,data=newdata)
    con = r.content
    if r.status_code == 200:
      endtime = time.time()
      print "Processed ："+str((endtime - starttime)*1000)+" ms"
      soup = BeautifulSoup(con)
      for tag in soup.find_all("script",{"src":False}):
          scripts = tag.text.encode('utf8')
          for _alert in scripts.split("\n"):
              if _alert.find("alert") > 0:
                  timeArray = time.localtime(time.time())
                  nowTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                  print str(nowTime) + str(_alert)
                 
                  return
    else:
      print r.status_code
      print r.content

def startLogin(headers,liteheaders,stkcode,cookiesPath):

    if os.path.isfile(cookiesPath):
        openCookiefile= open(cookiesPath,"r")
        cookies = openCookiefile.read()
        byOnlineResult = byOnline(headers,cookies,liteheaders,stkcode)
        #判断cookies是否过期
        if byOnlineResult == 1:
            cookies = getCookies(cookiesPath)
            login(cookies,cookiesPath)
    else:
      cookies = getCookies(cookiesPath)
      login(cookies,cookiesPath)
    return cookies


def byOnline(headers,cookies,liteheaders,stkcode):
    getHqHtml = paperBuyjsp(headers,cookies,liteheaders,stkcode)
    hardene = gethardene(getHqHtml)
    PriceLimit= getPriceLimit(getHqHtml)


    timeArray = time.localtime(time.time())
    nowTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    if hardene == None or PriceLimit == None:

          print str(nowTime)+" Cookies is void, Start "
          return 1
    else:
        print str(nowTime)+" : gtja is online...",hardene,PriceLimit

def run():
  stkcode = "300191"
  beginTime= time.strftime('%H%M%S',time.localtime(time.time()))

  cookies = startLogin(headers,liteheaders,stkcode,cookiesPath)
  t = getStockMsg.getStockMsg(0)
  flag = 0
  while int(beginTime) < 150001:
      gethardeneAPI(stkcode)
      thread.start_new_thread(byOnline,(headers,cookies,liteheaders,stkcode,))
      thread.start_new_thread(t.runloop,())
      if flag == 0:
        mailto_list=['328538688@qq.com']
        send_mail(mailto_list,"已启动","OK!")
        flag=1
      #获取当前时间，判断是否为下午3点
      beginTime= time.strftime('%H%M%S',time.localtime(time.time()))

      time.sleep(60)
  

if __name__ == '__main__':
  run()