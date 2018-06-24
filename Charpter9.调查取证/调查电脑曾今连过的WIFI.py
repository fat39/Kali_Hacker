from winreg import *
import os


def val2addr(val):
    addrlst = []
    for ch in val:
        addrlst.append(str(hex(ch))[-2:])
    MAC_ADDR = ':'.join(addrlst)
    return MAC_ADDR


def printNets():
    net = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged"
    key = OpenKey(HKEY_LOCAL_MACHINE, net)  # 提取注册表键值

    hostname = os.getenv('computername')  # 提取windows主机名
    print("计算机：" + hostname + " 游览过如下无线网络")
    for i in range(100):
        try:
            guid = EnumKey(key, i)  # 逐个提取key，最多100个
            netKey = OpenKey(key, str(guid))  # 打开key
            (n, addr, t) = EnumValue(netKey, 5)
            # print(n)#名字
            # print(addr)#内容
            # print(t)#类型
            (n, name, t) = EnumValue(netKey, 4)
            macAddr = val2addr(addr)  # 提取网关MAC
            SSID = str(name).strip()  # 企图SSID名字
            if SSID == '网络':
                CloseKey(netKey)
                next
            else:
                print("无线网络SSID名称: ", end='')
                print('%-20s' % SSID, end='')
                print('%25s' % '网关MAC地址: ', end='')
                print(macAddr)
                CloseKey(netKey)
        except Exception as e:
            # print(e)
            next


if __name__ == '__main__':
    printNets()