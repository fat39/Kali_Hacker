from TMALL_Def import *
from Spider_Def import SpiderDB

#创建数据库
spiderdb = SpiderDB('phone_tmall.sqlite')

#获取产品ID列表
productIdList = getProductIdList()

#获取第几个产品ID的编号
initial = 0

#异步获取数据的URL
url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=560065171365&spuId=889298324&sellerId=2838892713&order=3&currentPage=3&append=0&content=1&tagId=&posi=&picture=&ua=098%23E1hvRvvxvc%2BvUpCkvvvvvjiPPFqZQjnhPLLO0j3mPmPh6jrnPssUsjiERFSpQji8ROhCvCLwPUn%2BIYMwznsUgxSzkP1RzUC4946CvvyvmVW2eiIvAUvtvpvhvvvvvUhCvCLwMPDNmaMwzn1CFlS5IMsjzva4486CvCWICV0mEmpviVJHRFIA7g5x6X7tdphvhovWUgPdTQvydd7QrmtXAOcCRphvCvvvvvm5vpvhvvmv9FyCvvpvvvvv2QhvCvvvMMGEvpCWh2W8vvwS6fmYSCy4PvAyqU5E%2BdvdhU0HsXZpecifea7tFLu6b6V96fmYDb6sB8cBF4hZr0yoFOcnDBvOJ9kx6acEn1vDN%2BCld8Q7rbyCvm9vvvvhS6vvtQvvv0EvpvsCvvmjvhCvhRvvvUwvphvW5Qvvv0ivpvAfkphvC99vvOC0pTyCvv9vvUv1P8KEEphCvvOvCvvvphmjvpvhvvpvvvwCvvNwzHi4zM%2FidphvHLvUJ9EI4vmZWkeSEkDjdpeHsf7An86Cvvyvmhw2NzGvwwkrvpvEvvAvmB6avEcURphvCvvvvvv%3D&isg=BNfX7lu9QZHW58UwMhyD1BttZkshHKt-yiUJCSkFyqa5WPWaMO2kz_eSvvjGsIP2&needFold=0&_ksTS=1522508745259_2337&callback=jsonp2338'

while initial < len(productIdList):
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
                tmalljson = getJSONDetail(url,productId,num)
                #到到每一页的评论数量
                rateList = tmalljson['rateDetail']['rateList']

                #获取每一个产品,每一个评论页面,中的每一个评论信息
                n = 0
                while n < len(rateList):
                    #rateContent为评论内容
                    rateContent = rateList[n]['rateContent']
                    #colorSize格式:'网络类型:无需合约版;机身颜色:深空灰色;套餐类型:官方标配;存储容量:64GB'
                    colorSize = rateList[n]['auctionSku']
                    m = re.split('[:;]', colorSize)                    
                    color = m[3]
                    msize = m[7]
                    if '64G' in msize:
                        msize = '64GB'
                    elif '128G' in msize:
                        msize = '128GB'
                    elif '256G' in msize:
                        msize = '256GB'

                    #获取时间
                    dtime = rateList[n]['rateDate']
                    #写入数据库
                    spiderdb.insert(productId,color, msize, '天猫', rateContent, dtime)
                    spiderdb.commit()
                    n += 1
                num += 1
            except Exception as e:
                continue
        initial += 1
    except Exception as e:
        continue

spiderdb.close()