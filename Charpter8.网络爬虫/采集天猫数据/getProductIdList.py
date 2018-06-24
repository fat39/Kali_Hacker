from urllib3 import *
import json
import re
from Spider_Def import Read_Headers
from bs4 import BeautifulSoup

# 读取头部信息,主要是读取Cookie值
headers = Read_Headers('head_tm.txt')

# 忽略告警是一个不安全的选择,这样证书报错就会被略过
disable_warnings()

# PoolManager介绍,主要用于控制并发
# http://www.cnblogs.com/shadowwalker/p/5283372.html
http = PoolManager()


def getJSONDetail(url, itemId, currentPage):
    pass

def getLastPage(url,itemId):
    pass

def getProductIdList():
    # 搜索页面的URL
    url = 'https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.4.f01b2517hCRukj&q=mate10&start_price=3800&sort=d&style=g&search_condition=48&from=.list.pc_1_searchbutton&shopType=any&smAreaId=110100'

    # 请求URL,注意需要带上头部信息
    r = http.request('GET', url, headers=headers)
    # 使用GB18030解密,如果是偶数,基本能判断为GB18030
    c = r.data.decode('GB18030')

    # 使用BS分析数据
    soup = BeautifulSoup(c, 'lxml')

    #找打所有div,class等于product
    data_id_list = []
    div_product = soup.find_all('div', class_="product ")

    #在这些div中提取data-id
    for data_id in div_product:
        data_id_list.append(data_id.attrs['data-id'])

    return_id_list = []
    #再次发起请求确认产品为Mate10
    for item in data_id_list:
        url = 'detail.tmall.com/item.htm?id=' + item
        r = http.request('GET', url, headers=headers)
        r = r.data.decode('GB18030')
        soup = BeautifulSoup(r, 'lxml')
        # 找打div标签,并且class等于'tb-detail-hd'的文字部分
        item_name = soup.find('div', class_='tb-detail-hd').text
        if re.match('.*[Mm]ate\s*10.*', item_name.strip()):
            return_id_list.append(item)

    return return_id_list


if __name__ == '__main__':
    print(getProductIdList())
