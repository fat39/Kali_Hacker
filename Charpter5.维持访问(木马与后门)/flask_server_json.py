#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
#本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
#教主QQ:605658506
#亁颐堂官网www.qytang.com
#乾颐盾是由亁颐堂现任明教教主开发的综合性安全课程
#包括传统网络安全（防火墙，IPS...）与Python语言和黑客渗透课程！
from flask import Flask

from flask import request

import base64

import json

from datetime import datetime

node = Flask(__name__)



def b64_img(b64):
    b4code = bytes(b64,'utf8')

    img = base64.b64decode(b4code)

    return img

@node.route('/server_json', methods=['POST'])



def transaction():
  
  if request.method == 'POST':

    # 获取POST请求中的数据

    json_data = request.get_json()

    if json_data['MessageType'] == 'ImageEvent':        
        filename = datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'.bmp'
        recv_image = open(filename, 'wb')
        #print(json_data['Imageb64'])
        #print(b64_img(json_data['Imageb64']))
        recv_image.write(b64_img(json_data['Imageb64']))
        recv_image.close()
    else:
        print(json_data)

    return 'got data!!!'

if __name__ == '__main__':
    node.run(host = '0.0.0.0')