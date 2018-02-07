#coding=utf-8                                                                                 
import HTMLParser,urllib,urllib2,cookielib,json,time,re,datetime
from Parser import Parser
from Outputer import Outputer 

class Downloader(object):
    def download(self,url,data,headers):
        request = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(request)
        return response.read()


class SpiderMain(): #主程序
    def craw(self):
        headers = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                    "Cookie":"JSESSIONID=1F14C95743008150E0CCA865CFCE2B1D",
        }
        run_hour = time.strftime('%H',time.localtime(time.time()))
        run_hour = int(run_hour)
        if run_hour == 8:
            now_time = datetime.datetime.now()
            one_hour_before = now_time + datetime.timedelta(seconds = -43200)
            now_time = now_time.strftime('%Y-%m-%d %H:%M:%S') 
            one_hour_before = one_hour_before.strftime('%Y-%m-%d %H:%M:%S')
        else:
            now_time = datetime.datetime.now()
            one_hour_before = now_time + datetime.timedelta(seconds = -7200)
            now_time = now_time.strftime('%Y-%m-%d %H:%M:%S') 
            one_hour_before = one_hour_before.strftime('%Y-%m-%d %H:%M:%S') 


        post_url = "http://222.41.161.106:9106/asmx/install_report.asmx/SpiderUndo"
        detail_url = "http://10.134.73.41:9243/wms/analysis/sumAnalysisQuery1.do"
        
        test_data = {"page":1,"rows":"100","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"zj_zw","startTime":one_hour_before,"endTime":now_time,"orgIdSeq":"100000.610000.","dealuserId":"","accessWay":"other","queryFlag":"4","productType":"0"}
        html = Downloader.download(detail_url,urllib.urlencode(test_data),headers)
        string = json.loads(html)
        print string["pageObj"]["total"]
        pagenum = string["pageObj"]["total"]/100
        pagenum += 2
        i = 1
        while i < pagenum:
            test_data = {"page":i,"rows":"100","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"zj_zw","startTime":one_hour_before,"endTime":now_time,"orgIdSeq":"100000.610000.","dealuserId":"","accessWay":"other","queryFlag":"4","productType":"0"}
            html = Downloader.download(detail_url,urllib.urlencode(test_data),headers)
            html = json.loads(html)
            j=0
            while j < (len(html["list"])):
                html["list"][j]["sb_dz"] = html["list"][j]["sb_dz"].replace(","," ")
                html["list"][j]["WORK_ADDRESS"] = html["list"][j]["WORK_ADDRESS"].replace(","," ")
                j += 1
            html = json.dumps(html).decode('unicode_escape').encode('utf-8')
            post_data = {'text':html}
            Outputer.post_data_toT(post_url,post_data)
            time.sleep(20)
            i += 1


        test_data = {"page":1,"rows":"100","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"zt_zj_jy","startTime":"","endTime":"","orgIdSeq":"100000.610000.","dealuserId":"","accessWay":"other","queryFlag":"1","productType":"0"}
        html = Downloader.download(detail_url,urllib.urlencode(test_data),headers)
        string = json.loads(html)
        #test_data = {"page":1,"rows":"1000","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"zt_zj_jy","startTime":"","endTime":"","orgIdSeq":"100000.610000.","dealuserId":"","accessWay":"other","queryFlag":"1","productType":"40"}
        #html = Downloader.download(detail_url,urllib.urlencode(test_data),headers_test)
        print string["pageObj"]["total"]
        pagenum = string["pageObj"]["total"]/100
        pagenum += 2
        i = 1
        while i < pagenum:
            test_data = {"page":i,"rows":"100","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"zt_zj_jy","startTime":"","endTime":"","orgIdSeq":"100000.610000.","dealuserId":"","accessWay":"other","queryFlag":"1","productType":"0"}
            html = Downloader.download(detail_url,urllib.urlencode(test_data),headers)
            html = json.loads(html)
            j=0
            while j < (len(html["list"])):
                html["list"][j]["sb_dz"] = html["list"][j]["sb_dz"].replace(","," ")
                html["list"][j]["WORK_ADDRESS"] = html["list"][j]["WORK_ADDRESS"].replace(","," ")
                j += 1
            html = json.dumps(html).decode('unicode_escape').encode('utf-8')
            post_data = {'text':html}
            Outputer.post_data_toT(post_url,post_data)
            time.sleep(20)
            i += 1

        if run_hour != 8:
            today = datetime.datetime.today()
            one_hour_before = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
        test_data = {"page":1,"rows":"100","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"gd_zj_jg","startTime":one_hour_before,"endTime":now_time,"orgIdSeq":"100000.610000.","dealuserId":"","accessWay":"other","queryFlag":"2","productType":"0"}
        html = Downloader.download(detail_url,urllib.urlencode(test_data),headers)
        string = json.loads(html)
        #test_data = {"page":1,"rows":"1000","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"zt_zj_jy","startTime":"","endTime":"","orgIdSeq":"100000.610000.","dealuserId":"","accessWay":"other","queryFlag":"1","productType":"40"}
        #html = Downloader.download(detail_url,urllib.urlencode(test_data),headers_test)
        print string["pageObj"]["total"]
        pagenum = string["pageObj"]["total"]/100
        pagenum += 2
        i = 1
        while i < pagenum:
            test_data = {"page":i,"rows":"100","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"gd_zj_jg","startTime":one_hour_before,"endTime":now_time,"orgIdSeq":"100000.610000.","dealuserId":"","accessWay":"other","queryFlag":"2","productType":"0"}
            html = Downloader.download(detail_url,urllib.urlencode(test_data),headers)
            html = json.loads(html)
            j=0
            while j < (len(html["list"])):
                html["list"][j]["sb_dz"] = html["list"][j]["sb_dz"].replace(","," ")
                html["list"][j]["WORK_ADDRESS"] = html["list"][j]["WORK_ADDRESS"].replace(","," ")
                j += 1
            html = json.dumps(html).decode('unicode_escape').encode('utf-8')
            post_data = {'text':html}
            Outputer.post_data_toT(post_url,post_data)
            time.sleep(20)
            i += 1


        print "all complete"

if __name__ == "__main__":
    Downloader = Downloader()
    Parser = Parser()
    Outputer = Outputer()
    SpiderMain = SpiderMain()
    SpiderMain.craw()
