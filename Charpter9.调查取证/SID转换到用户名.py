from winreg import *

def sid2user(sid):
    try:
        location_key = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList" + '\\' + sid
        key = OpenKey(HKEY_LOCAL_MACHINE,location_key)#打开KEY
        (value, type) = QueryValueEx(key, 'ProfileImagePath')#查询'ProfileImagePath'的内容
        #value = C:\Users\现任明教教主
        user = value.split('\\')[-1]
        return user
    except:
        return sid

if __name__ == '__main__':
    print(sid2user('S-1-5-21-4051217124-2847813690-2809591918-1001'))
