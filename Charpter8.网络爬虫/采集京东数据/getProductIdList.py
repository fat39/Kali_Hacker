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
    pass

def getProductIdList():
    #搜索Mate,并且设置销量排序,和最低价格3800的URL
    url = 'https://search.jd.com/search?keyword=mate10&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=mate10&ev=exbrand_%E5%8D%8E%E4%B8%BA%EF%BC%88HUAWEI%EF%BC%89%5Eexprice_3800gt%5E&psort=4&click=0'
    r = http.request('GET',url,headers=headers)
    r = r.data
    soup = BeautifulSoup(r,'lxml')
    links = []
    idList = []
    #提取href内出现'//item.jd.com/'的标签
    tags = soup.find_all(href=re.compile('//item.jd.com/'))
    #提取所有href的内容,并且放入列表links中
    for tag in tags:
        links.append(tag['href'])

    #修剪URL得到单纯的产品ID
    for k in links:
        a = k.split('com/')
        idList.append(a[1].replace('.html','').replace('#comment',''))
    #使用集合消除重复内容
    idList = set(idList)
    return_id_list = []
    #再次访问产品页面,确保产品为Mate10
    for item in idList:
        url = 'https://item.jd.com/' + item + '.html'
        r = http.request('GET', url, headers=headers)
        r = r.data
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
    print(getProductIdList())
