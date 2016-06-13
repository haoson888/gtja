
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
import json


class wushan_1m1m():
    def __init__(self):
        self.host = "http://www.1m1m.com"
        self.DefaultUrl = "/Pages/LoginAndRegister.aspx?ru=/Pages/Default.aspx"
        self.loginUrl = ""
        self.ValidateCodeUrl = "/AjaxData/ValidateCodeData.ashx"
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

        self.proxies = {'http': '100.84.92.213:8889',
                    'https': '100.84.92.213:8889'}

    def getValidateCodeData(self,cookies):
        header={"Referer":self.host+self.DefaultUrl,
                "Accept": "image/webp,image/*,*/*;q=0.8",
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }
        imagefile = requests.get(self.host+self.ValidateCodeUrl,headers=header,cookies=cookies)
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

    def login(self):
        # cookies = requests.get(os.path.join(self.host,self.DefaultUrl))
        s = requests.Session()
        url=self.host+self.DefaultUrl
        r = s.get(url,proxies=self.proxies)
        loginHtml = r.content
        postBody = self.getPageInfo(loginHtml,"login")
        # print postBody
        cookies = r.cookies

        # print cookies
        postBody["ctl00$ContentPlaceHolder_Body$validateCodeTxb$txb"]= self.getValidateCodeData(cookies)
        print postBody

        url = self.host + self.DefaultUrl
        r = s.post(url,data=postBody,headers=self.headers,proxies=self.proxies)
        print r.status_code
        soup = BeautifulSoup(r.content)
        loginHtml = soup.findAll('span', {'class': "topLoginBar_content_name"})
        if loginHtml and len(loginHtml)>0:
            isLogin = loginHtml[0].text
            if isLogin == "18027187585":
                print "login sucessful"
                self.postwushan(s)
        else:
                time.sleep(5)
                self.login()

    def postwushan(self,s):
        # url = "http://www.1m1m.com/Pages/Reg/RegList.aspx?oid=1175&d=201606142"
        url = "http://www.1m1m.com/Pages/Reg/RegList.aspx?oid=1175&d=201606212"
        r = s.get(url)
        # print r.content
        postBody = self.getPageInfo(r.content,"wushan")
        time.sleep(5)
        r = s.post(url,data=postBody,headers=self.headers,proxies=self.proxies)
        print r.content
        soup = BeautifulSoup(r.content)
        result = soup.findAll('span', {'class': "regResult_failResult_reason_value"})
        if result:
            print result[0].text

    def parserBodyData(self,data):
        newdata = {}
        for line in data.split("\n"):
            key = line.split(": ")
            newdata[key[0]] = key[1]
        return newdata

    def checkwushan(self):
        url = "http://www.1m1m.com/AjaxData/Hospital/GetScheduleData.ashx"
        data = '''hospitalID: 2
sectionID: 483
doctorID: 867
outcallID: 1175
beginDate: 2016 - 06 - 13
endDate: 2016 - 06 - 21'''
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
        r = s.post(url,data=body,headers=newheader)
        jsonData =  r.json
        for i in (0,len(jsonData)):
            print jsonData[i]


if __name__ == '__main__':
    m= wushan_1m1m()
    # s= m.login()
    m.checkwushan()

# catp_url = 'http://www.1m1m.com/AjaxData/ValidateCodeData.ashx'
# imagefile = requests.get(catp_url)
# f = open('/Users/lylh/Desktop/capta.jpg','wb')
# f.write(imagefile.content)
# image = Image.open(StringIO(imagefile.content))
# vcode = pytesseract.image_to_string(image)
# print vcode
# if int(getConfig("CONFIG_DATA","captcha")) == 0 :
#       f = open('/Users/lylh/Desktop/capta.jpg','wb')
#       f.write(imagefile.content)
#       f.close()
# else:
#       image = Image.open(StringIO(imagefile.content))
#       vcode = pytesseract.image_to_string(image)
#       # print vcode
#       return vcode