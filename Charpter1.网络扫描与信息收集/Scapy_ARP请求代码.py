#!/usr/bin/python3
# -*- coding=utf-8 -*-

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)#清除报错
from scapy.all import *
from GET_IP_IFCONFIG import get_ip_address_ifconfig #获取本机IP地址
from GET_MAC import get_mac_address #获取本机MAC地址


def arp_request(ip_address, ifname = 'eth0'):
    #获取本机IP地址    
    localip = get_ip_address_ifconfig(ifname)['ip_address']
    #获取本机MAC地址
    localmac = get_mac_address(ifname)    
    try:#发送ARP请求并等待响应
        result_raw = srp(Ether(src=localmac, dst='FF:FF:FF:FF:FF:FF')/\
                          ARP(op=1, \
                               hwsrc=localmac, hwdst='00:00:00:00:00:00', \
                               psrc=localip, pdst=ip_address),\
                          iface = ifname, \
                          timeout = 1,\
                          verbose = False)
        #把响应的数据包对，产生为清单
        result_list = result_raw[0].res
        #[0]第一组响应数据包
        #[1]接受到的包，[0]为发送的数据包
        #获取ARP头部字段中的['hwsrc']字段，作为返回值返回
        return ip_address,result_list[0][1].getlayer(ARP).fields['hwsrc']
    except IndexError:
        return ip_address,None

if __name__ == "__main__":
    from optparse import OptionParser
    usage = "usage: ./scapy_arp_request ipaddress -i interface"
    version = "version 1.0"
    parser = OptionParser(usage=usage,version=version)
    parser.add_option("-i", "--interface", dest="iface",help="Specify an interface", default='ens160', type="string")
    (options, args) = parser.parse_args()
    if arp_request(args[0], options.iface)[1]:
        print(args[0]+' 的MAC地址为: '+arp_request(args[0], options.iface)[1])
    else:
        print('请确认主机:'+args[0]+' 是否存在')