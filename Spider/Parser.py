#coding=utf-8                                                                                 
import HTMLParser,urllib,urllib2,cookielib,json,time,re
class Parser(HTMLParser.HTMLParser):     #解析器，解析爬取的工单页面

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.key = {'td': None}
        self.res_data = []
 
    def clear_data(self):
        self.res_data = []
 
    def handle_starttag(self, tag, attrs): #处理开始标签，attrs代表标签a的属性 operthedog
        if tag == 'td':
            self.key['td'] = True
 
    def handle_data(self, data):
        if self.key['td']:
            data=data.strip('\n').strip()
            self.res_data.append(data)
            self.key['td'] = None
