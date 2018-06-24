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
    # 找到url中itemId,currentPage,callback内容
    re_result = re.match('.+itemId=(.+)&spuId.+&currentPage=(.+)&append.+callback=(.+)$', url).groups()
    url_itemId = re_result[0]
    url_currentPage = re_result[1]
    url_callback = re_result[2]

    # 替换itemId
    url = url.replace(url_itemId, str(itemId))
    # 替换currentPage
    url1 = url.split('&currentPage=')
    url2 = url.split('&append=')
    url = url1[0] + '&currentPage=' + str(currentPage) + '&append=' + url2[1]

    # 请求URL,注意需要带上头部信息
    r = http.request('GET', url, headers=headers)
    # 对内容进行GB18030的解码
    c = r.data.decode('GB18030')
    # 处理数据,以便于转换为JSON
    c = c.replace(url_callback + '(', '')
    c = c.replace(')', '')
    c = c.replace('false', '"false"')
    c = c.replace('true', '"true"')
    # 转换为JSON,并且返回
    tmalljson = json.loads(c)
    return tmalljson


def getLastPage(url,itemId):
    tmalljson = getJSONDetail(url,itemId, 1)
    return tmalljson['rateDetail']['paginator']['lastPage']


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
    # 异步获取数据的URL
    #url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=560065171365&spuId=889298324&sellerId=2838892713&order=3&currentPage=5&append=0&content=1&tagId=&posi=&picture=&ua=098%23E1hvTQvWvRyvUpCkvvvvvjiPPFqOsjnbRLF96jD2PmPUgj1UnLM91jrnnL590jEjRUhCvCB4cBHpRY147DiTPRwG5Dsu75MNh4wCvvpvvhHhkphvC9hvpyPOl8yCvv9vvhhFheZncfyCvm9vvhCmvvvvvvvvptWvvUhgvvCPLQvvv3QvvhYPvvmCGQvvBA6vvUHsmphvLvEK4eIaaXgqrqpyCWmQ%2Bu6fd5ln%2B87JeC94aymQ0fJ6W3CQog0HKfUpVcIUDaVTRLwpEcqWaXTQdfUf85xlHd8reC690f06W3vOfvyCvpvVvUCvpvvv2QhvCvvvMMGtvpvhvvCvpUwCvvpv9hCvdphvmpmCXVuFvvvUP2yCvvpvvhCv&isg=BIGB6CilvxEv1NN2eK6NurGfkM2brvWgUPe_T-PVuwiSyqacLP0tcjcoqD6MQo3Y&needFold=0&_ksTS=1522638863267_2000&callback=jsonp2001'
    # 任何一个Mate10的产品ID
    #itemId = '560027785687'
    # 获取这个Mate10产品ID的第一页评价内容
    #print(getJSONDetail(url, itemId, 1))
    #print(getLastPage(url, itemId))
