#!/usr/bin/env python
# -*- coding=utf-8 -*-
import socket
import threading
import time
import sys
import os
import struct


def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', 23456))  # 这里换上自己的ip和端口
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print("Waiting...")

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()


def deal_data(conn, addr):
    print('Accept new connection from {0}'.format(addr))
    while 1:
        fileinfo_size = struct.calcsize('128sl')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.strip(str.encode('\00'))
            new_filename = os.path.join(
                str.encode('./'), str.encode('new_') + fn)
            print('file new name is {0}, filesize if {1}'.format(
                new_filename, filesize))

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(new_filename, 'wb')
            print("start receiving...")
            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print("end receive...")
        conn.close()
        break


if __name__ == '__main__':
    socket_service()

# LOCAL_IP = '127.0.0.1'   #本机在局域网中的地址，或者写127.0.0.1
# PORT = 2567                   #指定一个端口
# def server():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.AF_INET 指ipv4  socket.SOCK_STREAM 使用tcp协议
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #设置端口
#     sock.bind((LOCAL_IP, PORT))       #绑定端口
#     sock.listen(3)                    #监听端口
#     while True:
#         sc,sc_name = sock.accept()    #当有请求到指定端口是 accpte()会返回一个新的socket和对方主机的（ip,port）
#         print('收到{}请求'.format(sc_name))
#         infor = sc.recv(1024)       #首先接收一段数据，这段数据包含文件的长度和文件的名字，使用|分隔，具体规则可以在客户端自己指定
#         length,file_name = infor.decode().split('|')
#         if length and file_name:
#             newfile = open('image/'+str(random.randint(1,10000))+'.jpg','wb')  #这里可以使用从客户端解析出来的文件名
#             print('length {},filename {}'.format(length,file_name))
#             sc.send(b'ok')   #表示收到文件长度和文件名
#             file = b''
#             total = int(length)
#             get = 0
#             while get < total:         #接收文件
#                 data = sc.recv(1024)
#                 file += data
#                 get = get + len(data)
#             print('应该接收{},实际接收{}'.format(length,len(file)))
#             if file:
#                 print('acturally length:{}'.format(len(file)))
#                 newfile.write(file[:])
#                 newfile.close()
#                 sc.send(b'copy')    #告诉完整的收到文件了
#         sc.close()
