from pandas import *
from matplotlib.pyplot import *
import sqlalchemy

#从数据库读取数据
engine_JD = sqlalchemy.create_engine('sqlite:///phone_jd_clear_done.sqlite')
engine_TMALL = sqlalchemy.create_engine('sqlite:///phone_tmall_clear_done.sqlite')

#设置字体,防止乱码
rcParams['font.sans-serif'] = ['SimHei']

#转换数据库数据到Pandas DataFrame格式
tmall_mate10_sales = read_sql('select color,size,source from phone_sales',engine_TMALL)
jd_mate10_sales = read_sql('select color,size,source from phone_sales',engine_JD)

#print(tmall_mate10_sales)
#print(jd_mate10_sales)

#合并天猫和京东数据
mate10_sales = concat([tmall_mate10_sales,jd_mate10_sales])

#print(mate10_sales)

#产生一个用数据来源排序的Pandas Series
datasourceCount = mate10_sales.groupby('source')['source'].count()
#print(datasourceCount)

#计算总体数量
allCount = datasourceCount.sum()
#print(allCount)

#转换Pandas Series对象到DataFrame对象(表)
datasource = datasourceCount.to_frame(name='数据来源')

#设置数据精度为小数点后两位
options.display.float_format='{:,.2f}%'.format

#在DataFrame对象中插入新列,插入的数据是百分比,并且使用上面的格式
datasource.insert(0,'比例',100*datasourceCount/allCount)

#使用matplotlib产生饼状图,并且保持数据精度为小数点后两位
datasource['数据来源'].plot(kind='pie',autopct='%.2f%%')
axis('equal')
legend()

show()

