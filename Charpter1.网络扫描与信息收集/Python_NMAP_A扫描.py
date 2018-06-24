#!/usr/bin/python3
# -*- coding=utf-8 -*-

import nmap
import sys
def nmap_A_scan(network_prefix):
    #创建一个扫描实例
    nm = nmap.PortScanner()
    #配置nmap扫描参数
    scan_raw_result = nm.scan(hosts=network_prefix, arguments='-v -n -A')   
    #分析扫码结果
    for host,result in scan_raw_result['scan'].items():
        if result['status']['state'] == 'up':
            print('#'*17 + 'Host:' + host + '#'*17)
            print('-'*20 + '操作系统猜测' + '-'*20)
            for os in result['osmatch']:
                print('操作系统为: ' + os['name'] + '   准确度为: ' + os['accuracy'])            
            idno = 1
            try:
                for port in result['tcp']:
                    try:
                        print('-'*17 + 'TCP服务详细信息' + '[' + str(idno) + ']' + '-'*17)
                        idno = idno + 1
                        print('TCP端口号:' + str(port))
                        try:
                            print('状态: ' + result['tcp'][port]['state'])
                        except:
                            pass
                        try:
                            print('原因: ' + result['tcp'][port]['reason'])
                        except:
                            pass
                        try:
                            print('额外信息: ' + result['tcp'][port]['extrainfo'])
                        except:
                            pass
                        try:
                            print('名字: ' + result['tcp'][port]['name'])
                        except:
                            pass
                        try:
                            print('版本: ' + result['tcp'][port]['version'])
                        except:
                            pass
                        try:
                            print('产品: ' + result['tcp'][port]['product'])
                        except:
                            pass
                        try:
                            print('CPE: ' + result['tcp'][port]['cpe'])
                        except:
                            pass
                        try:
                            print('脚本: ' + result['tcp'][port]['script'])    
                        except:
                            pass
                    except:
                        pass
            except:
                pass

            idno = 1
            try:
                for port in result['udp']:
                    try:
                        print('-'*17 + 'UDP服务详细信息' + '[' + str(idno) + ']' + '-'*17)
                        idno = idno + 1
                        print('UDP端口号:' + str(port))
                        try:
                            print('状态: ' + result['udp'][port]['state'])
                        except:
                            pass
                        try:
                            print('原因: ' + result['udp'][port]['reason'])
                        except:
                            pass
                        try:
                            print('额外信息: ' + result['udp'][port]['extrainfo'])
                        except:
                            pass
                        try:
                            print('名字: ' + result['udp'][port]['name'])
                        except:
                            pass
                        try:
                            print('版本: ' + result['udp'][port]['version'])
                        except:
                            pass
                        try:
                            print('产品: ' + result['udp'][port]['product'])
                        except:
                            pass
                        try:
                            print('CPE: ' + result['udp'][port]['cpe'])
                        except:
                            pass
                        try:
                            print('脚本: ' + result['udp'][port]['script'])    
                        except:
                            pass
                    except:
                        pass
            except:
                pass
            print('-'*20 + '地址详细信息' + '-'*20)
            try:
                print('IP地址: ' + result['addresses']['ipv4'])
                print('MAC地址: ' + result['addresses']['mac'])
            except:
                pass

if __name__ == '__main__':
    nmap_A_scan(sys.argv[1])