from urllib3 import *
from urllib.parse import urlsplit
from os.path import basename
import os

http = PoolManager()

def downloadImage(imgurls, folder):
    imgFileNames = []
    os.chdir(folder)
    print('开始下载文件....')
    for imgurl in imgurls:
        try:
            imgContent = http.request('GET',imgurl).data
            
            #print(urlsplit(imgurl))
            #SplitResult(scheme='http', netloc='www.qytang.com', path='/gps/gg_gps.jpg', query='', fragment='')
            imageFileName = basename(urlsplit(imgurl)[2])
            imageFile = open(imageFileName, 'wb')
            imageFile.write(imgContent)#写入文件内容
            imageFile.close()
            imgFileName = str(folder) + str(imageFileName)
            imgFileNames.append(imgFileName)#把写入的完整文件路径添加到清单imgFileNames
            
        except Exception as e:
            print(e)
            pass
    return imgFileNames

if __name__ == '__main__':
    imgurls = ['http://www.qytang.com/gps/gg_gps.jpg']
    print(downloadImage(imgurls, "C:\\Users\\Administrator\\"))