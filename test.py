
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
import requests,requests.utils, pickle
from StringIO import StringIO
from bs4 import BeautifulSoup
import smtplib
import ConfigParser
from email.mime.text import MIMEText
import getStockMsg,captcha
import json


class wushan_1m1m():
    def __init__(self):
        self.host = "http://www.1m1m.com"
        self.DefaultUrl = "/Pages/LoginAndRegister.aspx?ru=/Pages/Default.aspx"
        self.loginUrl = ""
        self.ValidateCodeUrl = "/AjaxData/ValidateCodeData.ashx"
        self.CenterUrl = "http://www.1m1m.com/Pages/Member/Center.aspx"
        self.headers = {
                 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                 "Origin": self.host,
                 "Upgrade-Insecure-Requests": "1",
                 "Content-Type": "application/x-www-form-urlencoded",
                 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
                 "Referer": "http://www.1m1m.com/Pages/Reg/RegList.aspx?oid=681&d=201606202"
                 }
        # self.proxies = {'http': '192.168.199.214:8888',
        #                 'https': '192.168.199.214:8888'}
        self.cookiesPath = self.cur_file_dir() + "/cookies";

        # self.proxies = {'http': '100.84.92.213:8889',
                    # 'https': '100.84.92.213:8889'}

        self.proxies = {'http': '117.185.122.205:8080',
                    'https': '117.185.122.205:8080'}

        self.cookies = self.isLogin()

    # 获取脚本文件的当前路径
    def cur_file_dir(self):
        # 获取脚本路径
        path = sys.path[0]
        # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
        if os.path.isdir(path):
            return path
        elif os.path.isfile(path):
            return os.path.dirname(path)

    def isLogin(self):

        if os.path.isfile(self.cookiesPath):

            # openCookiefile = open(self.cookiesPath, "r")
            # cookies = openCookiefile.read()
            with open(self.cookiesPath) as f:
                if f:
                    cookies = self.load_cookies(self.cookiesPath)
                else:

                    date = datetime.date.today()
                    self.login(str(date))
            s = requests.session()
            r = s.get(self.CenterUrl, cookies=cookies,proxies=self.proxies)
            print r.status_code
            # print r.content
            soup = BeautifulSoup(r.content)
            content_name = soup.findAll('span', {'class': "topLoginBar_content_name"})
            if content_name and content_name[0].text == "18027187585":
                return cookies
            else:
                date = datetime.date.today()
                self.login(str(date))

        else:
            date = datetime.date.today()
            self.login(str(date))

    def getValidateCodeData(self,cookies):
        header={"Referer":self.host+self.DefaultUrl,
                "Accept": "image/webp,image/*,*/*;q=0.8",
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }
        imagefile = requests.get(self.host+self.ValidateCodeUrl,headers=header,cookies=cookies,proxies=self.proxies)
        f = open('/Users/lylh/Desktop/capta.jpg', 'wb')
        f.write(imagefile.content)
        image = Image.open(StringIO(imagefile.content))
        vcode = pytesseract.image_to_string(image)
        print vcode
        return vcode

    def getPageInfo(self,responseBody,sys):
        soup = BeautifulSoup(responseBody)

        if sys == "login":
            infoList = ["__VIEWSTATE",
                        "__EVENTVALIDATION",
                        "__EVENTARGUMENT",
                        "ctl00$searchBar$searchTabValue",
                        "ctl00$searchBar$isCustomInput",
            ]
            postBody = {}
            postBody["__EVENTTARGET"] = "ctl00$ContentPlaceHolder_Body$loginSubmitBtn"
            # postBody["ctl00$ContentPlaceHolder_Body$outCallID"] = 1175
            # postBody["ctl00$ContentPlaceHolder_Body$beginTime"] = "2016 - 06 - 07 14:30:00"
            # postBody["ctl00$ContentPlaceHolder_Body$endTime"] = "2016 - 06 - 07 15:00:00"
            # postBody["ctl00$ContentPlaceHolder_Body$selectedScheduleID"] = "14:30 - 15:00"
            postBody["ctl00$searchBar$keyWordTxb"] = u"请输入医生、医院名称搜索（左边选择搜索类型）"
            postBody["ctl00$ContentPlaceHolder_Body$loginNameTxb$txb"]= 18027187585
            postBody["ctl00$ContentPlaceHolder_Body$loginPasswordTxb$txb"]="lylh1987"
        elif sys == "wushan":
            infoList = ["__VIEWSTATE",
                        "__EVENTVALIDATION",
                        "__EVENTARGUMENT",
                        "ctl00$searchBar$searchTabValue",
                        "ctl00$searchBar$isCustomInput",
                        # "ctl00$searchBar$keyWordTxb",
                        # "addOrModifyPatient_patientType",
                        # "addOrModifyPatient_gender",
                        # "addOrModifyPatient_idCardType",
                        # "addOrModifyMedicalInformation_payType",
                        # "regList_content_schedule_item_rdb",
                        # "regPatient_content_patients_item",

                        # "ctl00$ContentPlaceHolder_Body$beginTime",
                        # "ctl00$ContentPlaceHolder_Body$endTime",
                        # "ctl00$ContentPlaceHolder_Body$selectedScheduleFee",
                        # "ctl00$ContentPlaceHolder_Body$selectedScheduleID",
                        # "ctl00$ContentPlaceHolder_Body$hospitalID",
                        "ctl00$ContentPlaceHolder_Body$payOption"
                        ]
            postBody = {}
            postBody["__EVENTTARGET"] = "ctl00$ContentPlaceHolder_Body$regBtn"
            postBody["addOrModifyPatient_patientType"] = "on"
            postBody["addOrModifyPatient_gender"] = "on"
            postBody["addOrModifyPatient_idCardType"] = "on"
            postBody["regList_content_schedule_item_rdb"] = "on"
            postBody["regPatient_content_patients_item"] = "on"
            postBody["addOrModifyMedicalInformation_payType"] = "0"
            postBody["ctl00$ContentPlaceHolder_Body$hospitalID"]="2"
            postBody["ctl00$ContentPlaceHolder_Body$selectedScheduleFee"] = "9"
            postBody["ctl00$ContentPlaceHolder_Body$patientID"]=1098808
            postBody["ctl00$ContentPlaceHolder_Body$outCallID"] = 1175
            postBody["ctl00$ContentPlaceHolder_Body$beginTime"] = "2016-06-21 16:00:00"
            postBody["ctl00$ContentPlaceHolder_Body$endTime"] = "2016-06-21 16:30:00"
            postBody["ctl00$ContentPlaceHolder_Body$selectedScheduleID"] = "16:00-16:30"
            postBody["ctl00$searchBar$keyWordTxb"] = u"请输入医生、医院名称搜索（左边选择搜索类型）"
            # postBody["ctl00$ContentPlaceHolder_Body$loginNameTxb$txb"] = 18027187585
            # postBody["ctl00$ContentPlaceHolder_Body$loginPasswordTxb$txb"] = "lylh1987"

        for info in infoList:
            infoKey = soup.findAll('input', {'name': info})
            print info,infoKey
            if len(infoKey)>0:
                infoValue = infoKey[0]["value"]
                postBody[info]=infoValue
            else:
                postBody[info]=""


        return  postBody
        # EVENTVALIDATION = soup.findAll('input', {'id': '__EVENTVALIDATION'})
        # EVENTVALIDATION = EVENTVALIDATION[0]["value"]

    def save_cookies(self,requests_cookiejar, filename):
        with open(filename, 'wb') as f:
            pickle.dump(requests_cookiejar, f)

    def load_cookies(self,filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)


    def login(self,date):
        # cookies = requests.get(os.path.join(self.host,self.DefaultUrl))
        s = requests.Session()
        url=self.host+self.DefaultUrl
        r = s.get(url,proxies=self.proxies)
        loginHtml = r.content
        postBody = self.getPageInfo(loginHtml,"login")
        # print postBody
        cookies = r.cookies
        # with open(self.cookiesPath, 'w') as f:
        #     pickle.dump(requests.utils.dict_from_cookiejar(cookies), f)
        # print cookies
        postBody["ctl00$ContentPlaceHolder_Body$validateCodeTxb$txb"]= self.getValidateCodeData(cookies)
        url = self.host + self.DefaultUrl
        r = s.post(url,data=postBody,headers=self.headers,proxies=self.proxies)
        print r.status_code
        soup = BeautifulSoup(r.content)
        loginHtml = soup.findAll('span', {'class': "topLoginBar_content_name"})
        if loginHtml and len(loginHtml)>0:
            isLogin = loginHtml[0].text
            if isLogin == "18027187585":
                print "login sucessful"
                self.save_cookies(cookies, self.cookiesPath)
                self.postwushan(date,cookies)
                return 0

        else:
                time.sleep(5)
                self.login(str(date))

    def postwushan(self,date,cookies):
        # url = "http://www.1m1m.com/Pages/Reg/RegList.aspx?oid=1175&d=201606142"
        url = "http://www.1m1m.com/Pages/Reg/RegList.aspx?oid=1175&d="+str(date.replace("-",""))+"2"
        s = requests.session()
        r = s.get(url,cookies=cookies,proxies=self.proxies)
        # postBody = self.getPageInfo(r.content, "wushan")
        # time.sleep(5)
        # r = s.post(url, data=postBody, headers=self.headers, cookies=cookies, proxies=self.proxies)
        # soup = BeautifulSoup(r.content)
        # result = soup.findAll('span', {'class': "regResult_failResult_reason_value"})
        # # for tag in soup.find_all("script", {"src": False}):
        # #     scripts = tag.text.encode('utf8')
        # #     for _alert in scripts.split("\n"):
        # #         if _alert.find("errorMsgBox") == 1:
        # #             print str(_alert)
        # if result:
        #     print result[0].text
        if len(r.history) == 0 and r.status_code == 200:
                # print r.content
                postBody = self.getPageInfo(r.content,"wushan")
                time.sleep(5)
                r = s.post(url,data=postBody,headers=self.headers,cookies=cookies,proxies=self.proxies)
                soup = BeautifulSoup(r.content)
                result = soup.findAll('span', {'class': "regResult_failResult_reason_value"})
                if result:
                    print result[0].text
        else:
            date = datetime.date.today()
            self.login(str(date))

    def parserBodyData(self,data):
        newdata = {}
        for line in data.split("\n"):
            key = line.split(": ")
            newdata[key[0]] = key[1]
        return newdata

    def checkwushan(self):

        cookies = self.cookies
        url = "http://www.1m1m.com/AjaxData/Hospital/GetScheduleData.ashx"
        d1 = datetime.date.today()
        sevenDay = d1 + datetime.timedelta(8)
        data = '''hospitalID: 2
sectionID: 483
doctorID: 867
outcallID: 1175
beginDate: '''+str(d1)+'''
endDate: '''+str(sevenDay)+''''''
        body =self.parserBodyData(data)
        headers = '''Content-Length: 94
Accept: */*
Origin: http://www.1m1m.com
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Referer: http://www.1m1m.com/Pages/Hospital/Doctor.aspx?oid=1175
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'''
        newheader = self.parserBodyData(headers)
        s = requests.Session()
        r = s.post(url,data=body,headers=newheader,proxies=self.proxies)

        jsonData =  r.json()
        flag = 0
        if len(jsonData) >0:
            for i in range(0,len(jsonData)):
                wushanData =  jsonData[i]
                SectionName = wushanData["SectionName"]
                ScheduleItems= wushanData["ScheduleItems"][0]
                NumberCount = ScheduleItems["NumberCount"]
                TimePeriod = ScheduleItems["TimePeriod"]
                Date = wushanData['Date']
                Datestr = str(datetime.datetime.strptime(Date, "%Y-%m-%dT%H:%M:%S").date())
                if SectionName == u"按摩科" and int(NumberCount) > 0 and TimePeriod != u"晚上":
                # if SectionName == u"按摩科" and int(NumberCount) == 0 and TimePeriod != u"晚上":

                    if int(captcha.getConfig("CONFIG_DATA", "mail")) == 1:
                        mailto_list = ['328538688@qq.com']
                        captcha.send_mail(mailto_list, "wushan","wushan")
                        # s = m.login(Datestr)
                        self.postwushan(Datestr,cookies)
                        flag = 1
                        return 0

            if flag == 0:
                    timeArray = time.localtime(time.time())
                    nowTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    print str(nowTime) + " wushan is not NumberCount"



if __name__ == '__main__':

    m= wushan_1m1m()


    while True:
        try:
            m.checkwushan()
        except Exception, e:
            print str(e)
        time.sleep(5)

