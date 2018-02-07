#coding=utf-8                                                                                 
import HTMLParser,urllib,urllib2,cookielib,json,time,re,datetime
from Downloader import Downloader
from Parser import Parser
from Outputer import Outputer 

class SpiderMain(): #主程序
    def craw(self):
        test_url = "http://10.134.73.41:9214/wms/analysis/orderAnalysisListAjax.do"
        headers_test = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
        test_data = {"page":"1","rows":"100","orgId":"610000","busiType":"1","orderType":"1","startTime":"","endTime":"","workAction":"1","accessWay":"other","queryFlag":"1","productType":"40"}
        html = Downloader.download(test_url,urllib.urlencode(test_data),headers_test)
        result = re.findall(".*<label>账号</label>*",html)#是否跳转登陆页面
        
        if result:
            url = 'http://10.134.73.41:9214/cas/login?service=http%3A%2F%2F10.134.73.41%3A9214%2Fwms%2F%3Bjsessionid%3DC06AA8BF06F59C34B8D7B875C16ECBFD.w8'
            login_page = Downloader.getCookie_simple(url) 
            process_page = login_page[599:740]
            vcode_url = 'http://10.134.73.41:9214/cas/validateCodeServlet'
            Downloader.download_simple(vcode_url)
            cookie_string = login_page[login_page.find("jsessionid=")+11:login_page.find("?service=")]
            post_url = "http://10.134.73.41:9214/cas/login?service=http%3A%2F%2F10.134.73.41%3A9214%2Fwms%2F%3Bjsessionid%3D"+cookie_string
            post_data = {'lt':process_page[process_page.find("LT-"):process_page.find('" />')],'execution':process_page[process_page.find('value="e')+7:process_page.find('value="e')+11],'_eventId':'submit','username':'13991157290','password':'d65cc1719b49628ca1e6f269a0bdaeda','vcode':'请输入验证码','usernameTemp':'13991157290'}
            headers = {'Referer': 'http://10.134.73.41:9214/cas/login?service=http%3A%2F%2F10.134.73.41%3A9214%2Fwms%2F%3Bjsessionid%3D'+cookie_string,'Accept-Language':'zh-CN','User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; InfoPath.2)','Accept-Encoding':'gzip, deflate','Content-Length':'223','Connection':'Keep-Alive','Pragma':'no-cache'}
            Downloader.download(post_url,urllib.urlencode(post_data),headers)
            #test_url = "http://10.134.73.41:9214/wms/analysis/orderAnalysisListAjax.do"
            #headers_test = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
            #test_data = {"page":"1","rows":"100","orgId":"610000","busiType":"1","orderType":"1","startTime":"","endTime":"","workAction":"1","accessWay":"other","queryFlag":"1","productType":"40"}
            #html = Downloader.download(test_url,urllib.urlencode(test_data),headers_test)
        #print html
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
        detail_url = "http://10.134.73.41:9214/wms/analysis/sumAnalysisQuery1.do"
        

        test_data = {"page":1,"rows":"1000","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"zj_zw","startTime":one_hour_before,"endTime":now_time,"orgIdSeq":"100000.610000.","dealuserId":"","accessWay":"other","queryFlag":"4","productType":"40"}
        html = Downloader.download(detail_url,urllib.urlencode(test_data),headers_test)
        string = json.loads(html)
        print string["pageObj"]["total"]
        pagenum = string["pageObj"]["total"]/1000
        pagenum += 2
        i = 1
        while i < pagenum:
            test_data = {"page":i,"rows":"1000","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"zj_zw","startTime":one_hour_before,"endTime":now_time,"orgIdSeq":"100000.610000.","dealuserId":"","accessWay":"other","queryFlag":"4","productType":"40"}
            html = Downloader.download(detail_url,urllib.urlencode(test_data),headers_test)
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


        test_data = {"page":1,"rows":"1000","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"zt_zj_jy","startTime":"","endTime":"","orgIdSeq":"100000.610000.","dealuserId":"","accessWay":"other","queryFlag":"1","productType":"40"}
        html = Downloader.download(detail_url,urllib.urlencode(test_data),headers_test)
        string = json.loads(html)
        #test_data = {"page":1,"rows":"1000","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"zt_zj_jy","startTime":"","endTime":"","orgIdSeq":"100000.610000.","dealuserId":"","accessWay":"other","queryFlag":"1","productType":"40"}
        #html = Downloader.download(detail_url,urllib.urlencode(test_data),headers_test)
        print string["pageObj"]["total"]
        pagenum = string["pageObj"]["total"]/1000
        pagenum += 2
        i = 1
        while i < pagenum:
            test_data = {"page":i,"rows":"1000","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"zt_zj_jy","startTime":"","endTime":"","orgIdSeq":"100000.610000.","dealuserId":"","accessWay":"other","queryFlag":"1","productType":"40"}
            html = Downloader.download(detail_url,urllib.urlencode(test_data),headers_test)
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
        test_data = {"page":1,"rows":"1000","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"gd_zj_jg","startTime":one_hour_before,"endTime":now_time,"orgIdSeq":"100000.610000.","dealuserId":"","accessWay":"other","queryFlag":"2","productType":"40"}
        html = Downloader.download(detail_url,urllib.urlencode(test_data),headers_test)
        string = json.loads(html)
        #test_data = {"page":1,"rows":"1000","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"zt_zj_jy","startTime":"","endTime":"","orgIdSeq":"100000.610000.","dealuserId":"","accessWay":"other","queryFlag":"1","productType":"40"}
        #html = Downloader.download(detail_url,urllib.urlencode(test_data),headers_test)
        print string["pageObj"]["total"]
        pagenum = string["pageObj"]["total"]/1000
        pagenum += 2
        i = 1
        while i < pagenum:
            test_data = {"page":i,"rows":"1000","orgId":"610000","typeDto":"0","busiType":"0","orderType":"0","type":"gd_zj_jg","startTime":one_hour_before,"endTime":now_time,"orgIdSeq":"100000.610000.","dealuserId":"","accessWay":"other","queryFlag":"2","productType":"40"}
            html = Downloader.download(detail_url,urllib.urlencode(test_data),headers_test)
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
        #post_data = "lt=" + process_page[process_page.find("LT-"):process_page.find('" />')]+"&execution="+process_page[process_page.find('value="e')+7:process_page.find('value="e')+11]
        #post_data += "&_eventId=submit&username=13991157290&password=d65cc1719b49628ca1e6f269a0bdaeda&vcode=%E8%AF%B7%E8%BE%93%E5%85%A5%E9%AA%8C%E8%AF%81%E7%A0%81&usernameTemp=13991157290"
        #Outputer.post_data_toT(post_url,post_data)
        
        #print code_page
        #login_url = 'http://211.137.133.201:8080/ldims/liposs/system/loginmanage/LoginManageAction!getMessage.action?loginName=hz_lijian' 
        
        '''get_dynamicpassword_url='http://3.hzttweb.applinzi.com/Home/API/password'
        checkuser_url = r'http://211.137.133.201:8080/ldims/checkuser.jsp'
        checkuser_data = {'acc_loginname':'hz_lijian','area_name':'hzadmin.com'}
        headers = {'Referer': 'http://211.137.133.201:8080/ldims/login.jsp'}
        download_url = r'http://211.137.133.201:8080/ldims/liposs/service/faultlocation/faultPreJudge!judgement.action'
        post_data_toT_url = r'http://3.hzttweb.applinzi.com/Home/API/judge'
        unbundling_url = r'http://211.137.133.201:8080/ldims/liposs/service/faultlocation/faultPreJudge!modBindInfo.action'
        i = 0
        while i < (len(state_list)):
            download_post_data = urllib.urlencode({'username':state_list[i]['acc']})
            html = Downloader.download(download_url,download_post_data)
            result = re.findall(".*/ldims/login.jsp.*",html)#是否跳转登陆页面
            if result:
                Downloader.login(login_url)
                dynamicpassword = Downloader.get_dynamicpassword(get_dynamicpassword_url)
                checkuser_data['acc_password'] = dynamicpassword
                checkuser_data = urllib.urlencode(checkuser_data)
                Downloader.getCookie(checkuser_url,checkuser_data,headers) 
                continue
            html_cont = Outputer.get_info(html)
            if html_cont != 'False':
                if state_list[i]['op'] == '1':
                    Parser.feed(html_cont)
                    new_data = Parser.res_data
                    state_show = Outputer.data_process(new_data)
                    data = {'acc':state_list[i]['acc'],'content':state_show,'id':state_list[i]['id'],'userid':state_list[i]['userid']}
                    Outputer.post_data_toT(post_data_toT_url,data)
                if state_list[i]['op'] == '2':
                    unbundling_post_data = {'username':state_list[i]['acc'],'bindtype':99,'bindattr':''}
                    Outputer.unbundling(unbundling_url,unbundling_post_data)
                    unbundling_state = {"解绑状态":"修改绑定信息成功"}
                    state_show = json.dumps(unbundling_state,ensure_ascii=False, encoding="utf-8")
                    data = {'acc':state_list[i]['acc'],'content':state_show,'id':state_list[i]['id'],'userid':state_list[i]['userid']}
                    Outputer.post_data_toT(post_data_toT_url,data)
            else:
                state_info = {'用户状态':'此用户不存在！'}
                state_show = json.dumps(state_info,ensure_ascii=False, encoding="utf-8")
                data = {'acc':state_list[i]['acc'],'content':state_show,'id':state_list[i]['id'],'userid':state_list[i]['userid']}
                Outputer.post_data_toT(post_data_toT_url,data)
            i += 1
            Parser.clear_data()
                '''
if __name__ == "__main__":
    Downloader = Downloader()
    Parser = Parser()
    Outputer = Outputer()
    SpiderMain = SpiderMain()
    while 1: 
        now_hour = time.strftime('%H',time.localtime(time.time()))
        now_hour = int(now_hour)
        if  now_hour > 7  and now_hour < 23:
            SpiderMain.craw()
            print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) #打印时间 
            time.sleep(3600)
