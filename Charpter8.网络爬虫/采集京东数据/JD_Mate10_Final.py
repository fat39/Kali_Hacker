from Spider_Def import SpiderDB
from JD_Def import *

#创建数据库
spiderdb = SpiderDB('phone_jd.sqlite')

#获取产品ID列表
productIdList = getProductIdList()

#获取第几个产品ID的编号
initial = 0

#异步获取数据的URL
url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv5254&productId=5544014&score=0&sortType=5&page=7&pageSize=10&isShadowSku=0&rid=0&fold=1'

while initial < len(productIdList):
#while initial < 5:
    try:
        #逐个获取产品ID
        productId = productIdList[initial]
        print('----------------', str(productId), '----------------')

        #得到这个产品,评论页的最大页数
        maxnum = getLastPage(url,productId)

        #从第一页开始,逐页获取评论
        num = 1

        while num <= maxnum:
            try:
                jdDict = getJSONDetail(url,productId,num)
                #到到每一页的评论数量
                comments = jdDict['comments']

                #获取每一个产品,每一个评论页面,中的每一个评论信息
                n = 0
                while n < len(comments):
                    #获取评论内容
                    comment = comments[n]
                    
                    #获取客户评价
                    discuss = comment['content']
                    #获取产品颜色
                    productColor = comment['productColor']
                    #获取创建评价时间
                    creationTime = comment['creationTime']
                    #获取内存大小
                    productSize = comment['productSize']

                    #处理颜色中会出现内存大小的奇葩问题
                    if '64' in productColor:
                        productSize = '64GB'
                    elif '128' in productColor:
                        productSize = '128GB'
                    elif '256' in productColor:
                        productSize = '256GB'
                    
                    #处理内存大小为'标准版'的奇葩问题
                    if productSize == '标准版':
                        productSize = comment['productSales'][0]['saleValue']
                    elif '256' in productSize:
                        productSize = '256GB'
                    elif '64' in productSize:
                        productSize = '64GB'
                    elif '128' in productSize:
                        productSize = '128GB'

                    #如果内存大小和产品颜色都为空,需要读取referenceName
                    if productSize == '' and productColor == '':
                        productColor = comment['referenceName']

                    #写入数据库
                    spiderdb.insert(str(productId),productColor, productSize, '京东', discuss, creationTime)
                    spiderdb.commit()
                    n += 1

            except Exception as e:
                print(e)
                continue
            num += 1
        initial += 1

    except Exception as e:
        print(e)
        continue

spiderdb.close()