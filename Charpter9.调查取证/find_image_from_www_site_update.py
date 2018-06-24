from urllib3 import *
from bs4 import BeautifulSoup
import re

http = PoolManager()

def findImages(url):
    print('发现在URL上的图片文件: ' + url)
    urlContent = http.request('GET',url).data
    soup = BeautifulSoup(urlContent, "lxml")

    tags = soup.find_all('img')

    imgnames = []
    for tag in tags:
        imgnames.append(tag['src'])

    prefix = 'http://' + '/'.join(url.split('/')[2:-1]) + '/'

    img_urls = []

    for imgname in imgnames:
        img_urls.append(prefix + imgname)

    return img_urls

if __name__ == '__main__':
    print(findImages('http://www.qytang.com/gps/gps.html'))