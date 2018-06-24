import pygeoip

gi = pygeoip.GeoIP('C:\\Users\\Administrator\\Desktop\\quzheng\\GeoLiteCity.dat')#需要下载数据库到本地
def printRecord(tgt):
    rec = gi.record_by_name(tgt)
    city = rec['city']#城市名字
    country = rec['country_name']#国家名字
    long = rec['longitude']#经度
    lat = rec['latitude']#纬度
    print('[*] 目标:' + tgt + 'Geo定位结果！')
    print('[+] ' + str(city) + ', ' + str(country))
    print('[+] 纬度: ' + str(lat) + ', 经度: ' + str(long))

if __name__ == '__main__':
    printRecord('123.118.24.80') #IP地址
    printRecord('36.110.69.203')  #亁颐堂IP地址
    printRecord('23.105.195.20') #亁颐堂美国云服务器

###########################################################
# PS C:\Users\Administrator> python C:\Users\Administrator\Desktop\quzheng\from_ip_find_location.py
# [*] 目标:123.118.24.80Geo定位结果！
# [+] Beijing, China
# [+] 纬度: 39.9289, 经度: 116.38830000000002
# [*] 目标:23.105.195.20Geo定位结果！
# [+] Los Angeles, United States
# [+] 纬度: 34.04939999999999, 经度: -118.2641