import telnetlib,re,sys,time
from sys import argv

#进度条类
class ProgressBar:
    def __init__(self, count = 0, total = 0, width = 50,subtotal = 12,subcount = 0):
        self.count = count
        self.total = total
        self.width = width
        self.subtotal = subtotal
        self.subcount = subcount
        self.logname = "./log/%s log%s.txt"%(time.strftime('%Y-%m-%d',time.localtime(time.time())),sys.argv[2])
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
service-port<U><1,65535> \}:()23
>>User name:()xxxx
>>User password:()xxxxxx
HW-MA5\d{3}T>()enable
HW-MA5\d{3}T#()config
HW-MA5\d{3}T\(config\)#()interface  gpon %s/%s
HW-MA5\d{3}T\(config-if-gpon-%s/%s\)#()ont %s %s %s
HW-MA5\d{3}T\(config-if-gpon-%s/%s\)#()quit
HW-MA5\d{3}T\(config\)#()quit
HW-MA5\d{3}T#()quit
Are you sure to log out\? \(y/n\)\[n\]:()y'''%(oltip,frameid,slotid,frameid,slotid,option,portid,ontid,frameid,slotid)

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
                    break
        except:
            pass

    #关闭通道方法
    def kcloseme(self):
        self.kconobj.close()


if __name__=="__main__":
    #必要的实例化
    k = MyTelnet()
    #连接跳板
    k.telnetTxzOlt('172.24.67.2','autosend','hzwg20133')
    filename = "./ont" + sys.argv[2] + ".txt"
    f = open(filename,'r+').readlines()
    bar = ProgressBar(total = len(f))

    for line in f:
        bar.subcount = 0
        bar.move()
        ontinfo = line.strip('\n').split('/')
        k.telnetOlt(ontinfo[0],ontinfo[1],ontinfo[2],sys.argv[1],ontinfo[3],ontinfo[4])
    k.kcloseme
