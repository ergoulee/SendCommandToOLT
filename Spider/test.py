#coding=utf-8       
# import HTMLParser,urllib,urllib2,cookielib,json,time,re,datetime
import urllib,urllib2,time,datetime,json

# Downloader = Downloader()
url = "http://10.134.73.41:9243/wms/analysis/orderAnalysisQuery1.do"
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
headers = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie":"JSESSIONID=7D5442D92C1C404CB9181198CF4CC25E",
            }
# test_data = {"page":1,"rows":"20","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"zj_zw","startTime":"2018-02-07 14:03:59","endTime":"2018-02-07 15:03:59","orgIdSeq":"100000.610000.610100.","dealuserId":"","accessWay":"other","queryFlag":"4","productType":"0"}            
test_data = {"page":1,"rows":"2","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"zt_zj_jy","startTime":one_hour_before,"endTime":now_time,"orgIdSeq":"100000.610000.610100.","dealuserId":"","accessWay":"other","queryFlag":"4","productType":"0"}
# url = "http://10.134.73.41:9243/wms/analysis/orderAnalysisListAjax.do"
# test_data = {"page":"1","rows":"100","orgId":"610000","busiType":"1","orderType":"1","startTime":"","endTime":"","workAction":"1","accessWay":"other","queryFlag":"1","productType":"40"}
data = urllib.urlencode(test_data)
request = urllib2.Request(url, data, headers)
response = urllib2.urlopen(request)
html = response.read()
string = json.loads(html)
print string["pageObj"]["total"]