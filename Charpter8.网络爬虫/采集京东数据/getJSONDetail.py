from urllib3 import *
import json
import re
from Spider_Def import Read_Headers
from bs4 import BeautifulSoup

headers = Read_Headers('head_jd.txt')

#忽略告警是一个不安全的选择,这样证书报错就会被略过
disable_warnings()

#PoolManager介绍
#http://www.cnblogs.com/shadowwalker/p/5283372.html
http = PoolManager()

def getJSONDetail(url,productId,page):
    # 找到url中productId,page,callback内容
    re_result = re.match('.+callback=(.+)&productId=(.+)&score.+&page=(.+)&pageSize.+',url).groups()
    url_callback = re_result[0]
    url_productId = re_result[1]
    url_page = re_result[2]
    
    #替换productId
    url = url.replace(url_productId,str(productId))
    #替换page
    url1 = url.split('&page=')
    url2 = url.split('&pageSize')
    url = url1[0] + '&page=' + page + '&pageSize' + url2[1]

    # 请求URL,京东此处可以不用带头部
    r = http.request('GET', url)

    # 对内容进行GB18030的解码
    c = r.data.decode('GB18030')
    
    #此处测试过,不需要先解码为ISO-8859-1
    #c = r.data.decode('ISO-8859-1')
    
    # 处理数据,以便于转换为JSON
    c = c.replace(re_result[0] + '(', '')
    c = c.replace(');', '')
    c = c.replace('false', '"false"')
    c = c.replace('true', '"true"')

    # 转换为JSON,并且返回
    JDjson = json.loads(c)
    return JDjson

def getProductIdList():
    #搜索Mate,并且设置销量排序,和最低价格3800的URL
    url = 'https://search.jd.com/search?keyword=mate10&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=mate10&ev=exbrand_%E5%8D%8E%E4%B8%BA%EF%BC%88HUAWEI%EF%BC%89%5Eexprice_3800gt%5E&psort=4&click=0'
    r = http.request('GET',url,headers=headers)
    #京东个别页面使用GB18030解码会出现问题,所以使用更加通用的ISO-8859-1进行单字节解码
    #在特定需要中文转码的时候再采用GB18030解码
    r = r.data.decode('ISO-8859-1')
    soup = BeautifulSoup(r,'lxml')
    links = []
    idList = []
    #提取href内出现'//item.jd.com/'的标签
    tags = soup.find_all(href=re.compile('//item.jd.com/'))
    #提取所有href的内容,并且放入列表links中
    for tag in tags:
        links.append(tag['href'])
    #使用集合消除重复内容
    linkList = list(set(links))
    #修剪URL得到单纯的产品ID
    for k in linkList:
        a = k.split('com/')
        idList.append(a[1].replace('.html','').replace('#comment',''))

    return_id_list = []
    #再次访问产品页面,确保产品为Mate10
    for item in idList:
        url = 'https://item.jd.com/' + item + '.html'
        r = http.request('GET', url, headers=headers)
        r = r.data.decode('ISO-8859-1')
        soup = BeautifulSoup(r, 'lxml')
        #找打div标签,并且class等于'sku-name'的文字部分
        item_name = soup.find('div', class_='sku-name').text
        #如果文字中出现Mate 10关键字,就确认成功,写入最终返回的return_id_list中
        if re.match('.*[Mm]ate\s*10.*',item_name.strip()):
            return_id_list.append(item)

    return return_id_list

def getLastPage(url,productId):
    pass

if __name__ == '__main__':
    #print(getProductIdList())
    url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv140&productId=20045127777&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
    productId = '17215885416'
    print(getJSONDetail(url,productId,1))
