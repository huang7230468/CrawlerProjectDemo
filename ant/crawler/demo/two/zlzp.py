__author__ = 'Administrator'
# -*- coding: utf-8 -*-
import requests
import time
import pymongo
from  datetime import datetime
from bs4 import BeautifulSoup
from zhilian_kw_config import *
from multiprocessing import Pool
from itertools import product
from urllib.parse import urlencode


client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]


def download(url):
    header = {'User-Agent':'Mozilla/5.0(Windows NT 6.1;WOW64:rv:51.0) Gecko/20100101 Firefox/51.0'}
    response = requests.get(url,headers=header)
    response.encoding = 'utf-8'
    return response.text


def get_content(html):
    date = datetime.now().date()
    date = datetime.strftime(date,'%Y-%m-%d')
    soup = BeautifulSoup(html,'lxml')
    body = soup.body
    data_main = body.find('div',{'class':'newlist_list_content'})

    if data_main:
        tables = data_main.find_all('table')
        for i ,table_info in enumerate(tables):
            if i == 0:
                continue
            tds = table_info.find('tr').find_all('td')
            zwmc = tds[0].find('a').get_text() #职位名称
            zw_link = tds[0].find('a').get('href') #职位链接
            fkl = tds[1].find('span').get_text() #反馈率
            gsmc = tds[2].find('a').get_text() #公司名称
            zwyx = tds[3].get_text() #职位月薪
            gzdd = tds[4].get_text() #工作地点
            fbrq = tds[5].find('span').get_text() #发布日期

            tr_brief = table_info.find('tr',{'class':'newlist_tr_detail'})#招聘简介
            #print("tr_brief==="+str(tr_brief))
            brief = tr_brief.find('li',{'class':'newlist_deatil_last'}).get_text()
            #print("职位名称:"+str(zwmc))
            #print("职位月薪:"+str(zwyx))
            #print("工作地点:"+str(gzdd))
            #用生成器获取信息
            yield {'zwmc':zwmc,
                   'fkl':fkl,
                   'gsmc':gsmc,
                   'zwyx':zwyx,
                   'gzdd':gzdd,
                   'fbrq':fbrq,
                   'brief':brief,
                   'zw_link':zw_link,
                   'save_date':date
            }

def  main(args):
    basic_url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?'
    for keyword in KEYWORDS:
        mongo_table = db[keyword]
        paras = {'jl':args[0],
                 'kw':keyword,
                 'p':args[1]
        }
        url = basic_url + urlencode(paras)
        #print("url="+ url)
        html = download(url)
        #print("html="+html)
        if html:
            data = get_content(html)
            for item in data:
                #print("输出数据"+str(item))
                if mongo_table.update({'zw_link':item['zw_link']},{'$set':item},True):
                    print('已保存记录:',item)

if __name__ == '__main__':
    start = time.time()
    number_list = list(range(TOTAL_PAGE_NUMBER))
    print(number_list)
    args = product(ADDRESS,number_list)
    print(args)
    pool = Pool()
    pool.map(main,args)
    end = time.time()
    print('Finished,task runs %s seconds.'%(end-start))



