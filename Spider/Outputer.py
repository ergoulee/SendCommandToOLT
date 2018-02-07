#coding=utf-8                                                                                 
import HTMLParser,urllib,urllib2,cookielib,json,time,re
class Outputer(object):   #将含有告警清除时间的信息列表保存至文件
    def __init__(self):   #初始化数据
        self.datas=[]   
       
    def clear_data(self):
        self.datas=[]
    
    def get_info(self,html):
        #result = re.findall("<script.*</scrip>",html)
        temp = '无此用户'
        temp = temp.decode('utf-8').encode('gbk')
        html_temp = html.split('<tr>')
        html_cont = html_temp[7]+html_temp[8]+html_temp[9]+html_temp[13]
        result = re.findall(temp,html_cont)
        if result:
            print "此用户不存在！"
            return "False"
        return html_cont

    def data_process(self,data):    #data为获取到的html页面所包含的信息,data[0,12]均为无效数据
        state_info = {}
        config = ['认证时间','客户状态(正常/暂停/销户)','预判结果','开户时间']#这里做比较时，要都先转换成unicode类型
        for i in range(len(data)):
            data[i] = data[i].decode('gbk').encode('utf-8')
        for i in range(len(data)):
            if data[i] in config:
                state_info[data[i]]=data[i+1] #匹配上以后，转换成utf-8类型
        state_show = json.dumps(state_info,ensure_ascii=False, encoding="utf-8")
        return state_show
    def unbundling(self,url,values):
        file_name = './cookie.txt'    #保存cookie文件的路径
        cookie = cookielib.MozillaCookieJar()    #创建一个空的cookie实例对象
        cookie.load(file_name, ignore_discard=True, ignore_expires=True)   #从文件中读取cookie内容到cookie对象中
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        data = urllib.urlencode(values)
        i = 1
        while i < 10:
            try:
                req = urllib2.Request(url,data)
                response = opener.open(req)
                if response.getcode() == 200:
                    break
            except:
                time.sleep(3)
            i += 1  
            time.sleep(10)

    def post_data_toT(self,url,values):
        data = urllib.urlencode(values)
        i = 1
        while i < 10:
            try:
                req = urllib2.Request(url,data)
                response = urllib2.urlopen(req)
                if response.getcode() == 200:
                    break
            except:
                time.sleep(3)
            i += 1
            time.sleep(5)
        print response.read()
        time.sleep(1)
