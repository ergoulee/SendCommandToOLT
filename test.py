import telnetlib,re,sys,time

#进度条类
class ProgressBar:
    def __init__(self, count = 0, total = 0, width = 50,subtotal = 12,subcount = 0):
        self.count = count
        self.total = total
        self.width = width
        self.subtotal = subtotal
        self.subcount = subcount
        self.logname = "./log/%s log.txt"%time.strftime('%Y-%m-%d',time.localtime(time.time()))
        self.f = open(self.logname,'a')
    def move(self):
        self.count += 1
    def submove(self):
        self.subcount += 1
    def log(self, s = ''):
        sys.stdout.write(' ' * (self.width + 9) + '\r')
        sys.stdout.flush()
        if s != '':
            self.f.write("%s - log - %s \n"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),s))
        progress = self.width * self.subcount / self.subtotal
        progress = int(progress)
        sys.stdout.write('{0:3}/{1:3}: '.format(self.count, self.total))
        sys.stdout.write('#' * progress + '-' * (self.width - progress) + '\r')
        if (progress == self.width) and (self.count == self.total):
            sys.stdout.write('\n')
            self.f.close()
        sys.stdout.flush()

# Telnet连接类
class MyTelnet(object):

    # 实例化
    def __init__(self):
        self.kconobj=telnetlib.Telnet()

    # 登陆跳板
    def telnetTxzOlt(self,host,username,password):
        try:
            self.kconobj.open(host,23)
            self.kconobj.read_until(b'>>User name:',5)
            self.kconobj.write(username.encode('ascii') + b"\n")
            self.kconobj.read_until(b">>User password:")
            self.kconobj.write(password.encode('ascii') + b"\n")
        except:
            pass

    #移动olt登陆操作
    def telnetOlt(self,oltip,frameid,slotid,option,portid,ontid):
        mystr = '''SNHZ-912-OLT-TXZ01-HW-MA5680T>()telnet %s
{ <cr>|service-port<U><1,65535> }:()23
>>User name:()username
>>User password:()password
HW-MA5680T>()enable
HW-MA5680T#()config
HW-MA5680T\(config\)#()interface  gpon %s/%s
HW-MA5680T\(config-if-gpon-%s/%s\)#()ont %s %s %s
HW-MA5680T\(config-if-gpon-%s/%s\)#()quit
HW-MA5680T\(config\)#()quit
HW-MA5680T#()quit
Are you sure to log out? (y/n)[n]:()y'''%(oltip,frameid,slotid,frameid,slotid,option,portid,ontid,frameid,slotid)

        try:
            for line in mystr.splitlines():
                bar.submove()
                command = line.split('()')
                m = self.kconobj.expect([b".*%s$"%command[0].encode('ascii')],5)
                if m:
                    bar.log(m[2].decode('ascii'))
                    self.kconobj.write(command[1].encode('ascii') + b"\n")
                else:
                    bar.log(m[0:2]+"The expected value " + line + ", maybe timeout")
                    break
        except:
            pass

    #关闭通道方法
    def kcloseme(self):
        self.kconobj.close()

#定义一个菜单
def showmenu():

    print ('''


    *************** 操作选项 ***************

    1.批量去激活ONT
    2.批量激活ONT

    ''' )


if __name__=="__main__":

    #显示菜单
    showmenu()
    userinput = input("请输入你要执行的操作选项:")

    #必要的实例化
    k = MyTelnet()
    f = open("./str2.txt",'r+')
    count = len(f.readlines())
    bar = ProgressBar(total = count)
    #连接跳板
    k.telnetTxzOlt('1.1.1.1','username','password')

    while not userinput:
        userinput = input("请务必输入一个选项:")
    else:
        #提交主体命令区域,显示一些常用信息
        if userinput == '1':
            option = 'deactivate'
            for line in open("./str2.txt",'r+'):
                bar.subcount = 0
                bar.move()
                ontinfo = line.strip('\n').split('/')
                k.telnetOlt(ontinfo[0],ontinfo[1],ontinfo[2],option,ontinfo[3],ontinfo[4])
            k.kcloseme
        elif userinput == '2':
            option = 'activate'
            for line in open("./str2.txt",'r+'):
                bar.subcount = 0
                bar.move()
                ontinfo = line.strip('\n').split('/')
                k.telnetOlt(ontinfo[0],ontinfo[1],ontinfo[2],option,ontinfo[3],ontinfo[4])
            k.kcloseme
        else:
            print("选择错误")
