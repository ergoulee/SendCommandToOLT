import telnetlib,re,sys,time

#进度条类
class ProgressBar:
    def __init__(self, count = 0, total = 0, width = 50,subtotal = 10,subcount = 0):
        self.count = count
        self.total = total
        self.width = width
        self.subtotal = subtotal
        self.subcount = subcount
        self.logname = "./zxlog/%s log%s.txt"%(today,sys.argv[2])
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
        sys.stdout.flush()

# Telnet连接类
class MyTelnet(object):

    # 实例化
    def __init__(self):
        self.kconobj=telnetlib.Telnet()

    # 登陆跳板
    def telnetTxzOlt(self,host='172.24.67.2',username='autosend',password='hzwg20133'):
        try:
            self.kconobj.open(host,23)
            self.kconobj.read_until(b'>>User name:',5)
            self.kconobj.write(username.encode('ascii') + b"\n")
            self.kconobj.read_until(b">>User password:")
            self.kconobj.write(password.encode('ascii') + b"\n")
            bar.log("telnet TXZolt Success")
        except:
            pass

    #移动olt登陆操作
    def telnetOlt(self,oltip,frameid,slotid,portid,ontid,option):
        mystr = '''SNHZ-912-OLT-TXZ01-HW-MA5680T>()telnet %s 23
Username:()zte
Password:()KX!@#zte
ZX-C300#()configure terminal
ZX-C300\(config\)#()interface gpon-onu_%s/%s/%s:%s
ZX-C300\(config-if\)#()%s
ZX-C300\(config-if\)#()exit
ZX-C300\(config\)#()exit
ZX-C300#()exit'''%(oltip,frameid,slotid,portid,ontid,option)

        try:
            for line in mystr.splitlines():
                bar.submove()
                command = line.split('()')
                m = self.kconobj.expect([b".*%s$"%command[0].encode('ascii')],10)
                if m and m[1]:
                    bar.log(m[2].decode('ascii'))
                    self.kconobj.write(command[1].encode('ascii') + b"\n")
                else:
                    bar.log("The expected value " + line + ", maybe timeout")
                    self.kcloseme
                    self.telnetTxzOlt()
                    break
        except ZeroDivisionError as e:  
            print("try error " + line + e)
            self.kcloseme
            self.telnetTxzOlt()

    #关闭通道方法
    def kcloseme(self):
        self.kconobj.close()


if __name__=="__main__":
    #必要的实例化
    k = MyTelnet()
    #连接跳板
    k.telnetTxzOlt()
    filename = "./zxont" + sys.argv[2] + ".txt"
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    f = open(filename,'r+')
    #info = open("./log/%s optical-info.txt"%today,'a')
    fl = f.readlines()
    bar = ProgressBar(total = len(fl))
    if sys.argv[1] == "0":
        option = "shutdown"
    if sys.argv[1] == "1":
        option = "no shutdown"
    print(option)

    for line in fl:
        bar.subcount = 0
        bar.move()
        ontinfo = line.strip('\n').split('/')
        k.telnetOlt(ontinfo[0],ontinfo[1],ontinfo[2],ontinfo[3],ontinfo[4],option)
    k.kcloseme
    f.close()
bar.f.close()
