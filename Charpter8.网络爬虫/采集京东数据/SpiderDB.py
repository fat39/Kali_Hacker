import re
import os
import sqlite3

def Read_Headers(file):
    headerDict = {}
    f = open(file,'r')
    headersText = f.read()
    headers = re.split('\n',headersText)
    for header in headers:
        result = re.split(':',header,maxsplit=1)
        headerDict[result[0]] = result[1].strip()
    f.close()
    return headerDict

class SpiderDB:
    def __init__(self, dbname):
        self.dbname = dbname

        #如果数据库存在就删除这个数据库
        if os.path.exists(self.dbname):
            os.remove(self.dbname)

        conn = sqlite3.connect(self.dbname)
        self.conn = conn
        cursor = conn.cursor()
        self.cursor = cursor
        #创建数据库
        #1.id(唯一ID)
        #2.itemid(产品ID)
        #3.color(产品颜色)
        #4.size(内存大小)
        #5.source(数据源)
        #6.discuss(客户评论)
        #7.time(时间)
        self.cursor.execute("""create table phone_sales
                                (id integer primary key autoincrement not null,
                                itemid text not null,
                                color text,
                                size text,
                                source text not null,
                                discuss mediumtext not null,
                                time text not null);""")

    #插入数据
    def insert(self,itemid,color,size,source,discuss,time):
        self.cursor.execute('''insert into phone_sales(itemid,color,size,source,discuss,time)
                                      values('%s','%s','%s','%s','%s','%s')''' % (itemid, color, size, source, discuss, time))
    #提交数据
    def commit(self):
        self.conn.commit()
    #关闭连接
    def close(self):
        self.conn.close()

if __name__ == '__main__':
    spiderdb = SpiderDB('testdb.sqlite')
    spiderdb.insert('123123123','red','64','jd','testset','2018')
    spiderdb.insert('1231231232','red1','164','jd','testset','2018')
    spiderdb.commit()
    spiderdb.close()


