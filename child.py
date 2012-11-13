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

NUM_DICT = {}
#number of valid char
CHAR_NUM = 4



def LoginPageFromIE():
    '''
    login in the web page with username pwd and code
    '''
    ie = PAMIE()
    ie.navigate("https://epoint.pampers.com.cn/pages/rewards.aspx?r=5979") 
    #time.sleep(10)
    #return ie
    ie.textBoxSet('email','account')
    ie.textBoxSet('password', 'pwd')
    #Downloadcode(ie.cookieGet())
    #ie.textBoxSet('yzm',GetCode(CodeFilter()))
    #time.sleep(15)
    #ie.formSubmit('form1')
    ie.formSubmit('fmLogin')
    #ie.navigate("https://epoint.pampers.com.cn/pages/rewards_detail.aspx?p1=149") 
    ie.navigate("http://epoint.pampers.com.cn/pages/redeem.aspx?p1=149") 
    if ie.textBoxExists('password'):
        print 'fail to login in, please true again'
        return None    
    #ie.navigate('http://www.bjguahao.gov.cn/comm/kouqiang/ksyy.php?ksid=1040000&hpid=109')
    #print ie.pageGetText()
    #ie.javaScriptExecute(SetDocumentMode())
    #ie.javaScriptExecute('document.documentMode="7";')
    #ie.javaScriptExecute('document.write(document.getElementsByTagName("head"))')
    #ie.javaScriptExecute('document.getElementsByTagName(\'head\')[0].appendChild(\'<meta http-equiv="X-UA-Compatible" content="IE=7">\');')
    return ie


def LoginPage():
    '''
    login in the web page with username pwd and code
    '''  
    
    # Get login web page
    req = urllib2.Request('http://beijing.homelink.com.cn/webregister/login.php')
    opener = urllib2.urlopen(req)
    cookie = Cookie.SimpleCookie(opener.headers['set-cookie'])

    # get cookie info
    ret = ''
    for v in cookie.values():
        ret += "%s=%s; " % (v.key, v.value)
    #print ret

    # build headers
    headers = { 'Referer' : 'http://beijing.homelink.com.cn',
                'Cookie' : ret,
                'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}

    # get the valicode
    Downloadcode(headers)
    valicode = GetCode(CodeFilter())
    #print valicode

    # build Post data
    login_data = urllib.urlencode({'username' : '11111@qq.com',
                                   'password' : '1111',
                                   'validateCode': valicode,
                                   'dologin' : '登录'
                                   })

    # POST Login web page
    req.add_data(login_data)
    for (key, val) in headers.items():
        req.add_header(key,val)
    resp = urllib2.urlopen(req)
    content = resp.read()
    if content[:3]==codecs.BOM_UTF8:
        content = content[3:]    
    #print content
    #if content contains info "179095423", it's successful.
    #you are now logged in and can access "members only" content.
    #when your all done be sure to close it
    opener.close()
    resp.close()
    return headers



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


def Downloadcode(cookie,savefile='code.gif',url=r'http://epoint.pampers.com.cn/include/getCheckCode.aspx'):
    '''
    download code image from url
    '''
    import urllib2
    req = urllib2.Request(url)
    req.add_header("Cookie",cookie)
    req.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; Zune 4.7; MS-RTC LM 8; InfoPath.3; BRI/2)")
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
    print w, ' ', h
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
            

            
if __name__=='__main__':
    
    # for train to get valid code sample
    Train = False
    if Train:
        DownloadcodeForTrain()
        b_r = False
        (b_r, data) = GetNumFromCode(GetPreImage(CodeFilter()))
        if b_r:
            #TrainCode(data) # for train
            print GetCode(data) # get the code
        else:
            print 'failed'
        
    if not Train:
        # logon
        b_r = False
        code = ''
        ie = LoginPageFromIE()
        if ie!=None:
            while not b_r:
                # to complete with ?ticket=value, must be same ticket to submit.
                link = ie.linksGetValue('','')
                Downloadcode(ie.cookieGet(),url=link)
                (b_r, data) = GetNumFromCode(GetPreImage(CodeFilter()))
                if not b_r: continue
                code = GetCode(data)
            print code
            ie.textBoxSet('uxTextBoxCode',code)
            ie.formSubmit('form1')
                
