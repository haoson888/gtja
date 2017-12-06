#coding: utf-8
#date: 2015/12/28
#author: lylh

import requests
import captcha
import sys,re
import time,datetime
import json
import thread
from database_manager.sqliteoperator import DBDriver
reload(sys)
sys.setdefaultencoding("utf-8")



class getStockMsg():
    # def run(self):
    #     while True:
    #         time.sleep(1)
    def __init__(self,num):
        self.i = num
        self.message = ""
        self.flag=0
        self.dbfile = "/gtja.db"
       


    def getHistory(self,headers):
         url = "http://www.niuguwang.com/tr/201411/stocklistitem.ashx?version=2.4.7&packtype=0&s=App%20Store&usertoken=jQagMY41cB1ez7WqyhkszhMBXG2aGu2Iq-yMbevPecU*&id=18667530"
         r = requests.get(url=url, data="",headers = headers)
         comments = r.json()
         return  comments


    def getStock(self,i,follower):

        url = "http://www.niuguwang.com/foll/api/getfollowersall.ashx?version=2.2.1&packtype=0&pagesize=20&usertoken=jQagMY41cB1ez7WqyhkszhMBXG2aGu2Iq-yMbevPecU*&page="+str(i)+"&s=App%20Store"
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
            "Accept-Encoding": "gzip, deflate"}
        r =requests.get(url,headers=headers,timeout=5)
        harene = ""
        PriceLimit= ""
        historyData = self.getHistory(headers)
        followersMessageType = r.json()['data'][i]['followersMessageType']
        #followersMessageType，1为buy，2为sell
        if followersMessageType == 1 or followersMessageType == 2:
        # for i in range(0,len(r.json()['data'])):
        #     followersMessageType = r.json()['data'][i]['followersMessageType']
        #     if followersMessageType == 1 or followersMessageType == 2:
                userName = r.json()['data'][i]['userName']
                if userName in follower:
                        # for line in r.json()['data'][i]:
                        #     if type(r.json()['data'][i][line]) == "unicode":
                        #         print line +str(r.json()['data'][i][line].encode("utf8"))
                        #     else:
                        #         print line+": " +str(r.json()['data'][i][line])
                        # print followersMessageType
                        stockCode = r.json()['data'][i]['stockCode']
                        savemessage = r.json()['data'][i]['message']
                        stockName = r.json()['data'][i]['stockName']
                        print savemessage
                        m = re.match('.*?(\d+(\.\d+)?\%).*',savemessage)
                        if m:
                            percentage = m.group(1)
                            percentage = percentage.split("%")[0]
                        else:
                            percentage = 0
                        if historyData:
                            historyCount = historyData['stockListData'][0]['Position']
                        if self.message != percentage :
                            self.message = percentage
                            cookies= captcha.readCookies()
                            getHqHtml = captcha.paperBuyjsp(captcha.headers,cookies,captcha.liteheaders,stockCode)
                            PriceLimit,hardene,maxBuy,innercode,maxSell,lastAssets = captcha.gethardeneAPI(stockCode)
                            if followersMessageType == 1 and int(float(percentage))> 40:
                                # hardene = captcha.gethardene(getHqHtml)
                                print "hardene:"+str(hardene)
                                PriceLimit = 0
                            elif followersMessageType == 2 :
                                # PriceLimit= captcha.getPriceLimit(getHqHtml)
                                print "PriceLimit:"+ str(PriceLimit)
                                hardene = 0
                            else :
                                print "percentage:"+str(percentage)+" percentage not more than 40"
                                hardene = None
                                PriceLimit = None
                            if hardene or PriceLimit:
                                dbd = DBDriver(self.dbfile,("11","22"))
                                # captcha.PaperBuy(hardene,PriceLimit,headers,cookies,stockCode,followersMessageType,dbd)
                                for i in range(1,10):
                                    thread.start_new_thread(captcha.PaperBuy,(hardene,PriceLimit,headers,cookies,stockCode,followersMessageType,dbd,stockName,i,))
                                starttime = time.time()
                                captcha.simStockBuy(followersMessageType,hardene,PriceLimit,maxBuy,maxSell,innercode,lastAssets)
                                endtime = time.time()
                                print "simStockBuy Processed ："+str((endtime - starttime)*1000)+" ms"
                                if int(captcha.getConfig("CONFIG_DATA","mail")) ==1 :
                                    mailto_list=['328538688@qq.com']
                                    captcha.send_mail(mailto_list,savemessage,savemessage)
                            return
                        else:
                            timeArray = time.localtime(time.time())
                            nowTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                            if followersMessageType ==1 and int(float(percentage))> 40:
                                print str(nowTime) + " Already buy！！！！"
                                
                            elif followersMessageType ==2:
                                print str(nowTime) + " Already sell"
                            elif  int(float(percentage))< 40:
                                print str(nowTime) +" percentage:"+str(percentage)+" percentage not more than 40"
                            else:
                                print str(nowTime) + " No buying and selling information！"


                else:
                    timeArray = time.localtime(time.time())
                    nowTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    print str(nowTime) + " No buying and selling information！"

        else :
            timeArray = time.localtime(time.time())
            nowTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            print str(nowTime) + " No buying and selling information！"

    def runloop(self,follower):
        t = 0
        num = self.i
        while t < 60 :
            try:
                self.getStock(num,follower)
            except Exception, e:
                print str(e)
            time.sleep(1)
            t = t +1
        thread.exit()


# t = getStockMsg(6)
# t.getStock(6)
# for i in range(0,10):
# # i= 0
#     getStockMsg(i)
