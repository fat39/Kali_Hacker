from find_image_from_www_site_update import findImages
from download_image_from_www_site_update import downloadImage
from find_image_GPS import FindGPSimage
from os.path import basename

def download_findGPS(url):
    imgurls = findImages(url)#找到图片文件链接！
    print(imgurls)
    imgFileNames = downloadImage(imgurls, 'C:\\Users\\Administrator\\Download_IMG\\')
    #下载文件，并且返回文件清单！
    for img_downloaded in imgFileNames:#逐个分析图片的GPS信息
        print('='*20 + basename(img_downloaded) + '='*20)
        print(FindGPSimage(img_downloaded))

if __name__ == '__main__':
    download_findGPS('http://www.qytang.com/gps/gps.html')