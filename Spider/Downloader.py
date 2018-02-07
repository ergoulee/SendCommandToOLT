#coding=utf-8                                                                                 
import HTMLParser,urllib,urllib2,cookielib,json,time,re
class Downloader(object):     #下载含有告警信息的工单
    def download(self,url,data,headers):     #下载工单方法
        file_name = './cookie.txt'    #保存cookie文件的路径
        cookie = cookielib.MozillaCookieJar()    #创建一个空的cookie实例对象
        cookie.load(file_name, ignore_discard=True, ignore_expires=True)   #从文件中读取cookie内容到cookie对象中
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        i = 1
        while i < 10:
            try:   
                req = urllib2.Request(url,data,headers)
                response = opener.open(req)
                if response.getcode() == 200:
                    cookie.save(file_name, ignore_discard=True, ignore_expires=True)
                    break
            except:
                time.sleep(3)
            i += 1  
            time.sleep(10)
        return response.read()

    def download_simple(self,url):     #下载工单方法
        file_name = './cookie.txt'    #保存cookie文件的路径
        cookie = cookielib.MozillaCookieJar()    #创建一个空的cookie实例对象
        cookie.load(file_name, ignore_discard=True, ignore_expires=True)   #从文件中读取cookie内容到cookie对象中
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        i = 1
        while i < 10:
            try:   
                req = urllib2.Request(url)
                response = opener.open(req)
                if response.getcode() == 200:
                    break
            except:
                time.sleep(3)
            i += 1  
            time.sleep(10)
        return response.read()

    def getCookie_simple(self,url): #获取cookie
        file_name = './cookie.txt'
        cookie = cookielib.MozillaCookieJar(file_name)
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        i = 1
        while i < 10:
            try:
                req = urllib2.Request(url)
                response = opener.open(req)
                if response.getcode() == 200:
                    cookie.save(file_name, ignore_discard=True, ignore_expires=True)
                    break
            except:
                time.sleep(5)
            i += 1
            time.sleep(5)
        return response.read()

    def getCookie(self,url,data,headers): #获取cookie
        file_name = './cookie.txt'
        cookie = cookielib.MozillaCookieJar(file_name)
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        i = 1
        while i < 10:
            try:
                req = urllib2.Request(url,data,headers)
                response = opener.open(req)
                if response.getcode() == 200:
                    cookie.save(file_name, ignore_discard=True, ignore_expires=True)
                    break
            except:
                time.sleep(5)
            i += 1
            time.sleep(5)
    
    def login(self,url): #登录，发送动态密码
        i = 1
        while i < 10:
            try:
                response = urllib2.urlopen(url)
                if response.getcode() == 200:  #页面请求返回的状态值，200为请求成功
                    print response.read()                  
                    time.sleep(10)
                    break
            except:
                time.sleep(5)
            i += 1
            time.sleep(5)

    def get_info(self,url):
        i = 1
        while i < 10:
            try:
                response = urllib2.urlopen(url)   #打开铁通云平台包含sn_get流水列表的页面
                if response.getcode() == 200:     #页面打开成功退出循环
                    break
                print response.getcode()   
            except:
                time.sleep(3)
            i += 1
            time.sleep(5)
        return response.read()