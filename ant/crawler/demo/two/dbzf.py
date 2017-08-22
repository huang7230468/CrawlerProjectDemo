__author__ = 'Administrator'

import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from dbzf_config import *
import random
import pymongo
from ant.crawler.demo.util import ExcelUtil


class DBZF():

    def __init__(self):
        client = pymongo.MongoClient(MONGO_URI)
        self.db = client[MONGO_DB]
        self.ExcelUtils = ExcelUtil.ExcelUtil()

    def getPage(self,url):
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
        ##该ip会自动返回请求的ip地址
        #response = requests.get('http://icanhazip.com',headers=header,proxies={'http':random.choice(ACTIVE_IP)})
        ######此种配置
        #proxies = {'http':'http://180.156.249.225:53281'}
        #response = requests.get(url,headers=header,proxies=proxies)
        ######动态随机ip配置
        response = requests.get(url,headers=header,proxies={'http':random.choice(ACTIVE_IP)})
        #print(response.text)
        response.encoding = 'utf-8'
        return response.text

    def getPageContent(self,html):
        soup = BeautifulSoup(html,'html5lib')
        body = soup.body
        data_olt = body.find('table',{'class':'olt'})
        #data_olt = body.find('table',class_='olt')
        if data_olt:
            data_olt_tr = data_olt.find_all('tr',{'class':''})
            for i ,table_info in enumerate(data_olt_tr):
                if i == 0:
                    continue
                data_olt_a = table_info.find('a')
                data_olt_author = '' ;
                data_olt_replyAmount = '' ;
                data_olt_date = '' ;
                data_olt_nowrap = table_info.findAll('td',{'nowrap':'nowrap'})
                for j,data_olt_nowrap_info in enumerate(data_olt_nowrap):
                    if j == 0:
                        data_olt_author = data_olt_nowrap_info.get_text()
                    elif j == 1:
                        data_olt_replyAmount = data_olt_nowrap_info.get_text()
                    else:
                        data_olt_date = data_olt_nowrap_info.get_text()

                #html = self.getPage(data_olt_a['href'])
                htmlInner = self.getPage(data_olt_a['href'])
                detail = self.getNextPage(htmlInner)
                yield {
                    'room_href' : data_olt_a['href'],
                    'room_title' : data_olt_a['title'],
                    'room_author' : data_olt_author,
                    'room_replayAmount' : data_olt_replyAmount,
                    'room_Date' : data_olt_date,
                    'room_detail' : detail
                }
                #print(data_olt_a['href']+"===="+data_olt_a['title']+"====="+data_olt_author+"====="+data_olt_replyAmount+"====="+data_olt_date+"====="+detail)
        else:
            print("没有找到对应的房源数据")



        #查询子链接内容
    def getNextPage(self,html):
        #print("html============="+str(html))
        soup = BeautifulSoup(html,'html5lib')
        data = soup.find('div',{'class','topic-content'})
        if data:
            data_p = data.p
            if data_p:
                return data_p.get_text().replace('<br/>',' ').replace("\n", "")
            else:
                return ""


    def saveDate(self,item):
      mongo_table = self.db[COL_NAME]
      if mongo_table.update({'href':item['room_href']},{'$set':item},True):
          print('已保存记录:',item)

    def saveDataExcel(self,list):
        titles = ['room_href','room_title','room_author','room_replayAmount','room_Date','room_detail']
        self.ExcelUtils.buildExcel("dbzfExcel",list,titles)

    def main(self):
        basicUrl = "https://www.douban.com/group/shanghaizufang/";
        param = {
            'start' : 25
        }
        url = basicUrl +"?"+ urlencode(param)
        #print("请求的url"+url)
        html = self.getPage(url)
        if html:
          data = self.getPageContent(html)
          self.saveDataExcel(data)
          #for item in data:
          #    self.saveDate(item)

dbzf =  DBZF()

dbzf.main()