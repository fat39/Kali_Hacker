from urllib3 import *
import json
from urllib.parse import quote

disable_warnings()

http = PoolManager()

def WIFI_Location(BSSID_MAC):
    #https://wigle.net/account
    #通过上面的URL得到授权信息
    headers = {'Authorization':'Basic QUlEOGQwOTYwMDNjMWQyNzkzOWVmNjE2Yjg3NDVlZGFlNmI6Y2U1Yzg2OTNjMWIyNWJlN2NlOWFiMWE5YTMyOGU2OGY='}
    url = 'https://api.wigle.net/api/v2/network/search?onlymine=false&freenet=false&paynet=false&netid=' + quote(BSSID_MAC)
    r = http.request('GET',url,headers=headers)
    r = r.data.decode()

    JSON_DATA = json.loads(r)['results'][0]
    #print(JSON_DATA)
    return {'纬度':JSON_DATA['trilat'],'经度':JSON_DATA['trilong'],'国家':JSON_DATA['country'],'SSID':JSON_DATA['ssid']}

if __name__ == "__main__":
    print(WIFI_Location("12:02:8e:a1:2b:c9"))