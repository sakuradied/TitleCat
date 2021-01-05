import getopt
from urllib.request import urlopen
from urllib.request import Request
import re
import threading
import socket
import sys
import time
import socks
import ssl
# https://sakuradied.github.io/
# 啥都不会就会写bug！
ssl._create_default_https_context = ssl._create_unverified_context


def aboutme():
    print('''
        #####################################################
        #           _https://sakuradied.github.io         _ #
        # ___  __ _| | ___   _ _ __ __ _  __| (_) ___  __| |#
        #/ __|/ _` | |/ / | | | '__/ _` |/ _` | |/ _ \/ _` |#
        #\__ \ (_| |   <| |_| | | | (_| | (_| | |  __/ (_| |#
        #|___/\__,_|_|\_\\\__,_|_|  \__,_|\__,_|_|\___|\__,_|#
        #####################################################
    ''')

# 设置全局代理（PySocks）


def setPort(ip, port):
    print("代理设置中...")
    socks.set_default_proxy(socks.SOCKS5, str(ip), int(port))
    socket.socket = socks.socksocket
    testNetwork()


def testNetwork():
    try:
        req = Request("https://myip.ipip.net")
        testDta = urlopen(req, timeout=15)
        test = testDta.read()
        print(test.decode())
    except Exception as er:
        print(er)
        print("请检查代理是否可用")

# 读取UrlList内内容


def getUrls(httpx, urlDataFile, Timeout, useragent, threas):
    w = open(urlDataFile, "r")
    urlData = w.readlines()
    threas = int(threas)
    i = 0
    for url in urlData:
        url = url.rstrip("\n")
        if httpx == 'http':
            threading.Thread(target=getTitle, args=(
                "http://", url, Timeout, useragent,)).start()
        if httpx == 'https':
            threading.Thread(target=getTitle, args=(
                "https://", url, Timeout, useragent,)).start()
        if httpx == 'all':
            threading.Thread(target=getTitle, args=(
                "http://", url, Timeout, useragent,)).start()
            threading.Thread(target=getTitle, args=(
                "https://", url, Timeout, useragent,)).start()
        if i <= threas:
            i = i + 1
        else:
            time.sleep(int(Timeout)+3)
            i = 0
def getTitle(Type, urls, Timeout, useragent):
    StartTim = time.time()
    try:
        head = {'User-Agent': useragent}
        url = str(Type) + str(urls)
        req = Request(url, headers=head)
        htmlData = urlopen(req, timeout=Timeout)
        htmlData = htmlData.read()
        htmlData = htmlData.decode()
        getTitle = re.findall(r'<title>(.*)</title>', htmlData)
        EndTim = time.time()
        Time = EndTim - StartTim
        # print(htmlData)
        outputData(url, getTitle, Time)
    except Exception as er:
        outputERROR(url, er)


def outputData(urlText, titleText, timeoutData):
    print(urlText, titleText, timeoutData)


def outputERROR(url, errorData):
    pass
    #print(url, errorData)


def aboutHelp():
    print('''
        Help:
        -h,--help               获取帮助
        -f,--file               指定url列表文件
        -t,--timeout            设置超时等待时间(秒)
        -p,--proxy              设置代理服务器（目前仅支持sock5）[127.0.0.1:1080]
        -x,--httpx              指定为http或者https类型，默认为all [http，https,all]
        -u,useragent            设置UA头，默认为Windows Chrome85
        -s,-threas              设置同时线程数，默认为25
        -o,--output             设置输出路径（支持.txt与.csv）按输入后缀名进行检查
                                为空输出到当前目录List.txt下                  
        ''')
    sys.exit(2)


def about(argv):
    try:
        opts, args = getopt.getopt(
            argv, "f:ht:p:o:x:u:", ["file=", "help", "timeout=", "proxy=", "output=", "httpx=", "useragent="])
    except getopt.GetoptError:
        print("使用-h查看帮助")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-s" or opt == "--threas":
            threas = arg
        else:
            threas = 20
        if opt == "-u" or opt == "--useragent":
            try:
                useragent = int(arg)
            except Exception as er:
                print("使用-h查看帮助:", er)
                sys.exit(2)
        else:
            useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'

        if opt == "-x" or opt == "--httpx":
            if arg == "http" or arg == "https" or arg == "all":
                httpx = arg
            else:
                aboutme()
                print("参数错误请查看帮助")
                aboutHelp()
        else:
            httpx = 'all'

        # 设置timeout为空set10
        if opt == "-t" or opt == "--timeout":
            try:
                timeout = int(arg)
            except Exception as er:
                print(er)
                aboutHelp()
        else:
            timeout = 10

        # 设置Proxy代理
        if opt == "-p" or opt == "--proxy":
            ip = re.findall(
                r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", arg)
            port = re.findall(r":(\d.+)", arg)
            try:
                setPort(ip[0], port[0])
            except Exception as er:
                print(er)
                print("请检查输入的IP地址是否正确，如127.0.0.1:1080")
                aboutHelp()
        if opt == "-o" or opt == "--output":
            pass

    for opt, arg in opts:
        if opt == "-h" or opt == "--help":
            aboutHelp()

        if opt == "-f" or opt == "--file":
            getUrls(httpx, arg, timeout, useragent,threas)

if __name__ == "__main__":
    aboutme()
    about(sys.argv[1:])
