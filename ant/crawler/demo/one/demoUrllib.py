# coding:utf8
import urllib.request  ,urllib.parse ,urllib.error ,re

from bs4 import BeautifulSoup

if __name__=="__main__":

    print('====python3中urllib.request======')

    response = urllib.request.urlopen('https://www.baidu.com/')

    print(response.read())

    print (response)

    print('====python3中urllib.request.Request======')

    request = urllib.request.Request('https://www.baidu.com/')

    response = urllib.request.urlopen(request)

    print(response.read())

    print("==========模拟登陆==================")
    #urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)

    #values = {"username":"1016903103@qq.com","password":"XXXX"}

    #data = urllib.parse.urlencode(values)
    #url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
    #request = urllib.request.Request(url,data)
    #response = urllib.request.urlopen(request)
    #print(response.read())

    print("========丑事百科==========test===")


    file = open("result.html","w",encoding= 'utf8')
    pattern = re.compile('<div.*?author clearfix">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?'+
                         'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
    page = 1
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    url = 'https://www.qiushibaike.com/hot/page/' + str(page)
    try:
        request = urllib.request.Request(url,headers = headers)
        response = urllib.request.urlopen(request)
        #print (response.read().decode('utf-8'))
        data = response.read().decode('utf-8')

        try:
            items = re.findall(pattern,data)
            for item in items:
                print(item[3])

        except Exception  as err:
            print(err)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)

        if hasattr(e,"reason"):
            print(e.reason)








