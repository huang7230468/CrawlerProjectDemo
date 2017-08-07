__author__ = 'Administrator'

import  re ,urllib.request  ,urllib.error
#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self,str):
        str = re.sub(self.removeImg,"",str)
        str = re.sub(self.removeAddr,"",str)
        str = re.sub(self.replaceLine,"\n",str)
        str = re.sub(self.replaceTD,"\t",str)
        str = re.sub(self.replacePara,"\n    ",str)
        str = re.sub(self.replaceBR,"\n",str)
        str = re.sub(self.removeExtraTag,"",str)
        #strip()将前后多余内容删除
        return str.strip()

class BDTB:
    def __init__(self,baseUrl,SeelZ):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(SeelZ)
        self.tool = Tool()


    #传入页码，获取该页帖子的代码
    def getPage(self,pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' +str(pageNum)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            return response.read().decode('utf-8')
        except urllib.error as e:
            if hasattr(e,'reason'):
                print( u"连接百度贴吧失败,错误原因",e.reason)
                return  None

    def getTitle(self):
        page = self.getPage(1)
        pattern = re.compile('<h1 class="core_title_txt.*?">(.*?)</h1>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None


    def getPageNum(self):
        page = self.getPage(1)
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getContent(self,page):
        pattern = re.compile('<div id="post_content_.*?">(.*?)</div>',re.S)
        items = re.findall(pattern,page)
        print (self.tool.replace(items[1]))



baseURL = 'http://tieba.baidu.com/p/5260223270'
bdth = BDTB(baseURL,1)
bdth.getContent(bdth.getPage(1))
