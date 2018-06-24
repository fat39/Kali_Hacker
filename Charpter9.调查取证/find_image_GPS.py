import exifread
import re
def FindGPSimage(filepath):
    GPS = {}
    Date = ''
    f = open(filepath, 'rb')
    tags = exifread.process_file(f)
    for tag,value in tags.items():
        if re.match('GPS GPSLatitudeRef', tag):
            GPS['GPSLatitudeRef'] = str(value)
        elif re.match('GPS GPSLongitudeRef', tag):
            GPS['GPSLongitudeRef'] = str(value)
        elif re.match('GPS GPSAltitudeRef', tag):
            GPS['GPSAltitudeRef'] = int(str(value))
        elif re.match('GPS GPSLatitude', tag):
            try:
                match_result = re.match('\[(\w*), (\w*), (\w.*)/(\w.*)\]', str(value)).groups()
                GPS['GPSLatitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])/int(match_result[3])
            except:
                GPS['GPSLatitude'] = str(value)
        elif re.match('GPS GPSLongitude', tag):
            try:
                match_result = re.match('\[(\w*), (\w*), (\w.*)/(\w.*)\]', str(value)).groups()
                GPS['GPSLongitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])/int(match_result[3])
            except:
                GPS['GPSLongitude'] = str(value)
        elif re.match('GPS GPSAltitude', tag):
            GPS['GPSAltitude'] = str(value)
        elif re.match('.*Date.*', tag):
            Date = str(value)
    return {'GPS信息':GPS, '时间信息':Date}
    #http://www.gpsspg.com/maps.htm
if __name__ == '__main__':
    print(FindGPSimage("C:\\Users\\Administrator\\gps_test.jpg")) 

###########################运行结果###############################
# PS C:\Users\Administrator> python C:\Users\Administrator\Desktop\quzheng\find_image_GPS.py
# {'GPS信息': {'GPSLongitude': (116, 18, 2.17), 'GPSLatitudeRef': 'N', 'GPSLongitudeRef': 'E', 'GPSLatitude': (40, 4, 2.26)}, '时间信息': '2018:04:04 22:34:21'}