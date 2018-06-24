#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import os

filelist = os.listdir()

#print(filelist)

img_no_list = []

for x in filelist:
    if 'PNG' in x:
        img_no = x[3:-4]
        img_no_list.append(int(img_no))

img_no_list.sort()

#print(img_no_list)
y = 1

for x in img_no_list:
    filename = '幻灯片' + str(x) + '.PNG'
    finalname = str(y) + '.PNG'
    os.rename(filename,finalname)
    y += 1