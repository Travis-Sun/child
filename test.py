# -*- coding:utf-8;-*-

import time, re
from cPAMIE import PAMIE
from sgmllib import SGMLParser
import urllib, urllib2, cookielib, Cookie, codecs
import threading
from time import ctime, sleep
from Queue import Queue
from random import randint
from datetime import date
import threading
from random import randrange

NUM_DICT = {}
#number of valid char
CHAR_NUM = 4
URL = r'http://epoint.pampers.com.cn/include/getCheckCode.aspx'
ASPXAUTH = ''
ASPNET_SESSIONID = ''
USER = 'tinny414@sohu.com'
PWD = 'Zh0uwei!'
TO_MAILS = ['sc369963@gmail.com',]
NTHREAD = 10
NIE = 3

import logging

# 创建一个logger
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
#ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
#logger.addHandler(ch)

# 记录一条日志
#logger.info('foorbar')



def LoginPageFromIE():
    '''
    login in the web page with username pwd and code
    '''
    global USER
    global PWD
    ie = PAMIE()
    ie.navigate("http://epoint.pampers.com.cn/pages/rewards.aspx?r=5979")
    #print ie.cookieGet()
    #time.sleep(10)
    #return ie
    ie.textBoxSet('email',USER) #account
    ie.textBoxSet('password', PWD) #pwd
    #Downloadcode(ie.cookieGet())
    #ie.textBoxSet('yzm',GetCode(CodeFilter()))
    #time.sleep(15)
    #ie.formSubmit('form1')
    ie.formSubmit('fmLogin')
    #ie.navigate("http://epoint.pampers.com.cn/pages/redeem.aspx?p1=149") 
    while ie.textBoxExists('password'):
        print 'fail to login in, try again'
        #ie.navigate("http://epoint.pampers.com.cn/pages/rewards.aspx?r=5979")
        ie.textBoxSet('email',USER) #account
        ie.textBoxSet('password', PWD) #pwd
        ie.formSubmit('fmLogin')
        logger.info('try login')
    ie.navigate("http://epoint.pampers.com.cn/pages/redeem.aspx?p1=149")        
    logger.info('login ok')
    #print ie.cookieGet()
    # prepare to in
    ie.javaScriptExecute('javascript:alert("plese input the ASPXAUTH and ASP.net_Session")')
    logger.info('input session info')
    #print 'input ASPXAUTH value'
    global ASPXAUTH
    ASPXAUTH = raw_input('ASPXAUTH=')
    #print 'input asp.net_sessionid value'
    global ASPNET_SESSIONID
    ASPNET_SESSIONID = raw_input('ASPNET_SESSIONID=')
    #ie.navigate("http://epoint.pampers.com.cn/pages/rewards_detail.aspx?p1=149") 
    #ie.navigate("http://epoint.pampers.com.cn/pages/redeem.aspx?p1=149")     
    #print ie.pageGetText()
    #ie.javaScriptExecute(SetDocumentMode())
    #ie.javaScriptExecute('document.documentMode="7";')
    #ie.javaScriptExecute('document.write(document.getElementsByTagName("head"))')    
    return ie


def LoginPage():
    '''
    login in the web page with username pwd and code
    '''  
    
    # Get login web page
    #req = urllib2.Request('http://epoint.pampers.com.cn/system/login2.aspx')
    req = urllib2.Request('http://epoint.pampers.com.cn')
    opener = urllib2.urlopen(req)
    cookie = Cookie.SimpleCookie(opener.headers['set-cookie'])

    # get cookie info
    ret = ''
    for v in cookie.values():
        ret += "%s=%s; " % (v.key, v.value)
    #print ret
    #ret += "%s=%s; " %('.ASPXAUTH',ASPXAUTH)
    #ret += "%s=%s; " %('ASP.NET_SessionId',ASPNET_SESSIONID)

    # build headers
    headers = { 'Referer' : 'http://epoint.pampers.com.cn/',
                'Cookie' : ret,
                'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}

    # get the valicode
    #Downloadcode(headers)
    #valicode = GetCode(CodeFilter())
    #print valicode

    # build Post data
    login_data = urllib.urlencode({'email' : USER,
                                   'password' : PWD,
                                   'fromweb': 'ECRM',
                                   'url' : 'https://epoint.pampers.com.cn/system/action.aspx?u=http%3a%2f%2fepoint.pampers.com.cn%2findex.aspx%3fr%3d634902949235714406'
                                   })

    # POST Login web page
    req = urllib2.Request('http://epoint.pampers.com.cn/system/login2.aspx')
    req.add_data(login_data)
    for (key, val) in headers.items():
        req.add_header(key,val)
    resp = urllib2.urlopen(req)
    content = resp.read()
    if content[:3]==codecs.BOM_UTF8:
        content = content[3:]    
    print content
    #if content contains info "179095423", it's successful.
    #you are now logged in and can access "members only" content.
    #when your all done be sure to close it
    opener.close()
    resp.close()
    #return headers



def OpenWebPage(url,headers):
    '''
    read the content of web page
    '''
    req = urllib2.Request(url, headers=headers)
    opener = urllib2.urlopen(req)
    content = opener.read()
    if content[:3]==codecs.BOM_UTF8:
        content = content[3:]    
    #print content
    opener.close()
    return content


def Downloadcode(cookie,savefile='code.gif',url=URL):
    '''
    download code image from url
    '''
    import urllib2
    #url = url + '?ticks=' + str(int(time.time()*1000))
    #URL = url
    #print url
    global ASPXAUTH
    global ASPNET_SESSIONID
    #print ASPXAUTH,'\n', ASPNET_SESSIONID
    #print cookie
    cookie += "; %s=%s" %('.ASPXAUTH',ASPXAUTH)
    cookie += "; %s=%s" %('ASP.NET_SessionId',ASPNET_SESSIONID)
    #print cookie
    req = urllib2.Request(url)
    req.add_header("Cookie",cookie)
    req.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; Zune 4.7; MS-RTC LM 8; InfoPath.3; BRI/2)")
    try:
        res_img = urllib2.urlopen(req)
        f = open(savefile, 'wb')
        f.write(res_img.read())
        f.close()
    except:
        res_img = urllib2.urlopen(req)
        f = open(savefile, 'wb')
        f.write(res_img.read())
        f.close()        


def DownloadcodeForTrain(savefile='code.gif',url=r'http://epoint.pampers.com.cn/include/getCheckCode.aspx'):
    '''
    download code image from url
    '''
    import urllib2
    req = urllib2.Request(url)
    #req.add_header("Cookie", cookie)
    req.add_header("Referer", 'http://epoint.pampers.com.cn')
    res_img = urllib2.urlopen(req)
    f = open(savefile, 'wb')
    f.write(res_img.read())
    f.close()


def CodeFilter(fromfile='code.gif', tofile='code_temp.png'):
    '''
    pre-process the image.
    '''
    import Image,ImageEnhance,ImageFilter, ImageDraw
    import sys
    image_name = 'code.gif'
    im = Image.open(image_name)
    im_new = im.convert('L')    
    draw = ImageDraw.Draw(im_new)
    draw.line((0, 0, im.size[0], 0), fill=0)
    draw.line((0, 0, 0, im.size[1]), fill=0)
    draw.line((0, im.size[1]-1, im.size[0], im.size[1]-1), fill=0)
    draw.line((im.size[0]-1, 0, im.size[0]-1, im.size[1]-1), fill=0)
    enhancer = ImageEnhance.Brightness(im_new)
    im_new = enhancer.enhance(2.0) 
    enhancer = ImageEnhance.Contrast(im_new)
    im_new = enhancer.enhance(9) 
    im_new.convert('1')
    im_new.filter(ImageFilter.MedianFilter)
    im_new.save(tofile)
    return im_new


def TrainCode(data, sname='code.txt'):
    '''
    train the data
    '''
    import pickle
    fh = open(sname,'a')    
    for s in data:
        #print pickle.dumps(s)
        fh.write(repr(pickle.dumps(s)))
        fh.write('\n')                
    fh.close()


def GetCode(data):
    '''
    get the four code numbers.
    '''
    retVal = ''
    b_r = True
    LoadCodeFromTrain()    
    for s in data:
        max_f = 0
        temp_char = ''
        for k in NUM_DICT:
            v = NUM_DICT[k]
            f = float(len(v&s))/float(len(v|s))
            if f>max_f:
                max_f = f
                temp_char = k            
        retVal += temp_char
    return retVal

def GetPreImage(im):
    '''
    image resolve matrix
    '''
    import Image, ImageDraw 
    w,h = im.size
    #print w, ' ', h
    data = []
    #im = img.load()
    im.save('precode.png')
    img = Image.open('precode.png')
    draw = ImageDraw.Draw(img)
    for i in range(w):
        temp = []
        for j in range(h):
            if j==5: temp.append(0)
            #print i,' ',j, ' ', im.getpixel((i,j))            
            if i==0 or j==0 or i==w-1 or j==h-1:
                #print i,' ',j, ' ', im.getpixel((i,j))            
                if j>6-1 and j<h-6: temp.append(0)
                draw.point((i,j),fill=0)
                continue
            num_zero = 0
            if im.getpixel((i,j))!=255:
                #print i,' ',j, ' ', im.getpixel((i,j))            
                if j>6-1 and j<h-6: temp.append(0)
                draw.point((i,j),fill=0)
                continue
            if im.getpixel((i-1,j))==255: num_zero += 1
            if im.getpixel((i+1,j))==255: num_zero += 1
            if im.getpixel((i,j-1))==255: num_zero += 1
            if im.getpixel((i,j+1))==255: num_zero += 1
            if num_zero>1:
                #print i,' ',j, ' ', im.getpixel((i,j))            
                if j>6-1 and j<h-6: temp.append(1)
                draw.point((i,j),fill=255)
            else:
                #print i,' ',j, ' ', im.getpixel((i,j))            
                if j>6-1 and j<h-6: temp.append(0)
                draw.point((i,j),fill=0)
        data.append(temp)
    img.save("precode.png")
    return data


def PreMatrix(data):
    '''
    get connection pixel set
    '''
    list_s = []
    for w in range(len(data)):
        for h in range(len(data[0])):
            #print '(%d, %d)' %(w,h)
            if data[w][h]==1 and data[w][h-1]==0 and data[w-1][h]==0:
                s = set()                
                s.add((w,h))
                list_s.append(s)
            if data[w][h]==1 and data[w][h-1]==1:
                for si in range(len(list_s)):
                    if (w,h-1) in list_s[si]:
                        list_s[si].add((w,h))
            if data[w][h]==1 and data[w-1][h]==1:
                for si in range(len(list_s)):
                    if (w-1,h) in list_s[si]:
                        list_s[si].add((w,h))
        for h in range(len(data[0])):
            first_s = -1
            for si in range(len(list_s)):                
                #print si
                #print list_s[si]
                if (w,h) in list_s[si]:
                    if first_s>-1:
                        list_s[first_s] = list_s[si] | list_s[first_s]
                        list_s[si].clear()
                    else:
                        first_s =si
    
    return [sorted(s) for s in list_s if s]
        

def GetNumFromCode(data):
    list_s = PreMatrix(data)
    list_return = []
    if len(list_s)!=4: return (False, list_s)
    for i in range(len(list_s)):
        temp_s = set()
        min_x = min(list_s[i])[0]
        for it in range(len(list_s[i])):
            temp_s.add((list_s[i][it][0]-min_x,list_s[i][it][1]))
        list_return.append(temp_s)
    return (True, list_return)
    

def LoadCodeFromTrain(fName='code.txt'):
    import pickle
    with open(fName) as f:
        for line in f:
            #print line
            (val, key) = line.split()
            #print key
            #print pickle.loads(eval(key))
            NUM_DICT[key] = pickle.loads(eval(val))

def SendMail(data,subject):
    global TO_MAILS
    import smtplib
    from email.MIMEText import MIMEText
    fromaddr = 'sc369963@gmail.com'  
    toaddrs  = TO_MAILS

    msg = MIMEText(data, 'plain','gb2312')
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = ";".join(toaddrs)
    #msg = 'There was a terrible error that occured and I wanted you to know!'  
  
  
    # Credentials (if needed)  
    username = 'sc369963@gmail.com'  
    password = 'sc369963'  
    
    # The actual mail send  
    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.starttls()  
    server.login(username,password)  
    server.sendmail(fromaddr, toaddrs, msg.as_string())  
    server.quit()

            

def Submit(ie):
    b_r = False
    code = ''
    
    ie.navigate("http://epoint.pampers.com.cn/pages/redeem.aspx?p1=149") 
    while not b_r:
        # to complete with ?ticket=value, must be same ticket to submit.
        #ie.linkClick('regCodeImg')
        #link = ie.linkGetValue('regCodeImg','src')
        #print link
        Downloadcode(ie.cookieGet())
        (b_r, data) = GetNumFromCode(GetPreImage(CodeFilter()))
        if not b_r: continue
        code = GetCode(data)
    #print code
    ie.textBoxSet('uxTextBoxCode',code)
    #time.sleep(10)
    #ie.formSubmit('form1')
    ie.buttonImageClick('ImgbtnRedeem')
    return ie

def ThreadFunction(threadID):
    ie = PAMIE()
    ie = Submit(ie)
    bTry = True
    while bTry:
        print 'id:%d try again.--%s' %(threadID,time.strftime('%Y-%m-%d %H:%M:%S'))
        Hour_now = time.strftime('%H')
        if int(Hour_now)> 18 or int(Hour_now) < 8:
            time.sleep(1800)
            ie = Submit(ie)
            localURL = ie.locationURL()
            if localURL.find('error')>0 or localURL.find('redeem')>0:
                bTry = True
            else:
                bTry = False
            #ie.elementExists('span','id','Lerror')
    print 'id:%d is OK' % threadID
    #SendMail('http://epoint.pampers.com.cn','have book the customer')
    ie.quit()

def submit2(ie, code):
    b_r = False
    code = ''    
    
    while not b_r:
        # to complete with ?ticket=value, must be same ticket to submit.
        #ie.linkClick('regCodeImg')
        #link = ie.linkGetValue('regCodeImg','src')
        #print link
        Downloadcode(ie.cookieGet())
        (b_r, data) = GetNumFromCode(GetPreImage(CodeFilter()))
        if not b_r: continue
        code = GetCode(data)
    #print code
    ie.textBoxSet('uxTextBoxCode',code)
    #time.sleep(10)
    #ie.formSubmit('form1')
    ie.buttonImageClick('ImgbtnRedeem')
    return ie

def initSubmit2(N):
    ieclass = []
    threads = []
    def ThreadFunc():
        ie = PAMIE()
        ie.navigate("http://epoint.pampers.com.cn/pages/redeem.aspx?p1=149")
        ieclass.append(ie)
    for i in range(N):
        t = threading.Thread(target=ThreadFunc)
        threads.append(t)

    for i in range(N):
        threads[i].start()

    for i in range(N):
        threads[i].join()

    return ieclass

def PrepareSubmit3(N):
    ieclass = []
    logger.info('open %d ie' %N)
    for i in range(N):
        ie = PAMIE()
        ie.navigate("http://epoint.pampers.com.cn/pages/redeem.aspx?p1=149")
        ieclass.append(ie)
    return ieclass

def validCode(ie):
    b_r = False
    code = ''
    logger.info('to get the code')
    while not b_r:
        # to complete with ?ticket=value, must be same ticket to submit.
        #ie.linkClick('regCodeImg')
        #link = ie.linkGetValue('regCodeImg','src')
        #print link
        Downloadcode(ie.cookieGet())
        (b_r, data) = GetNumFromCode(GetPreImage(CodeFilter()))
        if not b_r: continue
        code = GetCode(data)
    logger.info('the code is %s' %code)
    return code
    
def fillCode(ieclass, code):
    threads = []
    def ThreadFunc(ie, code):
        ie.textBoxSet('uxTextBoxCode',code)
    for ie in ieclass:
        t = threading.Thread(target=ThreadFunc, args=(ie,code))
        threads.append(t)
    for i in range(len(ieclass)):
        threads[i].start()

    for i in range(len(ieclass)):
        threads[i].join()

        
def submitThread(ieclass):
    threads = []
    def ThreadFunc(ie):
        ie.buttonImageClick('ImgbtnRedeem')
        time.sleep(60)
        ie.quit()

    for ie in ieclass:
        t = threading.Thread(target=ThreadFunc, args=(ie,))
        threads.append(t)
    for i in range(len(ieclass)):
        threads[i].start()        
        time.sleep(10)

def submitPage(ie,id):
    logger.info('before thread %d submit' %id)
    ie.buttonImageClick('ImgbtnRedeem')
    logger.info('after thread %d submit' %id)
    #time.sleep(10)

def gobackPage(ie,id):
    logger.info('before thread %d go back' %id)
    ie.javaScriptExecute('history.back()')
    logger.info('after thread %d go back' %id)
                
            
if __name__=='__main__':
    
    # for train to get valid code sample
    Train = False
    #LoginPageFromIE()
    if Train:
        DownloadcodeForTrain()
        b_r = False
        (b_r, data) = GetNumFromCode(GetPreImage(CodeFilter()))
        if b_r:
            #TrainCode(data) # for train
            print GetCode(data) # get the code
        else:
            print 'failed'
        
    if False and not Train:
        # logon
        ie = LoginPageFromIE()
        ie = Submit(ie)
        bTry = True
        while bTry:
            print 'try again.--', time.strftime('%Y-%m-%d %H:%M:%S')
            Hour_now = time.strftime('%H')
            if int(Hour_now)> 18 or int(Hour_now) < 8:
                time.sleep(1800)
            ie = Submit(ie)
            localURL = ie.locationURL()
            if localURL.find('error')>0 or localURL.find('redeem')>0:
                bTry = True
            else:
                bTry = False
            #ie.elementExists('span','id','Lerror')
        print 'OK'
        #SendMail('http://epoint.pampers.com.cn','have book the customer')
        ie.quit()
    # run thread
    if False:
        ie = LoginPageFromIE()
        for i in range(NTHREAD):
            p = threading.Thread(target=ThreadFunction, args=(i,))
            p.start()
            time.sleep(110/NTHREAD)
    
    if False:
        ie = LoginPageFromIE()
        #ie = PAMIE()
        print NIE
        while(True):
            ieclass = PrepareSubmit3(NIE)
            code  = validCode(ie)
            fillCode(ieclass,code)
            submitThread(ieclass)

    
    if True:
        logger.info('start')
        ie = LoginPageFromIE()        
        N = 3        
        ieclass = PrepareSubmit3(N)

        raw_input('wait for ie')
        code = validCode(ie)
        threads = []

        logger.info('to fill the code')
        for ie in ieclass:
            ie.textBoxSet('uxTextBoxCode',code)
            
        logger.info('to start %d thread to submit' %N)
        ii = 0
        for ie in ieclass:
            #ie.textBoxSet('uxTextBoxCode',code)
            t = threading.Thread(target=submitPage,args=(ie,ii))
            t.start()
            ii += 1
        
        time.sleep(60)

        ii = 0
        for ie in ieclass:
            #ie.textBoxSet('uxTextBoxCode',code)
            t = threading.Thread(target=gobackPage,args=(ie,ii))
            t.start()
            ii += 1
        
        
        if False:
            for ie in ieclass:
                ie.buttonImageClick('ImgbtnRedeem')
                
            for ie in ieclass:
                ie.javaScriptExecute('history.back()')
                    
            for ie in ieclass:
                ie.buttonImageClick('ImgbtnRedeem')

