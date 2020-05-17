# -*- coding: utf8 -*-

import socket
import os
import struct


def get_filelist(PATH):
    PATH = os.getcwd() + "\\pics"
    filelist = []
    for root, dirs, files in os.walk(PATH, topdown=False):
        for name in files:
            str2 = os.path.join(root, name)
            # print(name)
            if name.split('.')[-1] == 'jpg' and name.split('_')[0] == 'pic':
                filelist.append(str2)
    return filelist

# print(filelist)


def sendingPics():
    host = '140.116.96.107'  # 對server端為主機位置
    port = 5555
    address = (host, port)
    count = 0
    filelist = get_filelist(PATH)
    for filepath in filelist:
        count += 1
        socket02 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # AF_INET:默認IPv4, SOCK_STREAM:TCP
        socket02.connect(address)  # 用來請求連接遠程服務器

        ##################################
        # 開始傳輸
        # print('start send image')
        print("----------------------")
        print("Sending Pic ", count)
        while 1:
            if os.path.isfile(filepath):
                # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
                fileinfo_size = struct.calcsize('128sl')
                # 定义文件头信息，包含文件名和文件大小
                fhead = struct.pack('128sl', bytes(os.path.basename(
                    filepath).encode('utf-8')), os.stat(filepath).st_size)
                socket02.send(fhead)
                # print('client filepath: {0}'.format(filepath))
                fp = open(filepath, 'rb')
                while 1:
                    data = fp.read(1024)
                    if not data:
                        print('{0} file send over...'.format(
                            os.path.basename(filepath)))
                        break
                    socket02.send(data)
            socket02.close()
            break
        print(os.path.basename(filepath), 'finished! ')


# imgFile = open("1.png", "rb")
# while True:
#     imgData = imgFile.readline(512)
#     if not imgData:
#         break  # 讀完檔案結束迴圈
#     socket02.send(imgData)
# imgFile.close()

# #!/usr/bin/env python
# # -*- coding=utf-8 -*-

# import socket
# import os
# import sys
# import struct


# def socket_client():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.connect(('140.116.96.107', 23456))
#     except socket.error as msg:
#         print(msg)
#         sys.exit(1)

#     print(s.recv(1024))

# while 1:
#     filepath = input("please input file path: ")

#     if os.path.isfile(filepath):
#         # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
#         fileinfo_size = struct.calcsize('128sl')
#         # 定义文件头信息，包含文件名和文件大小
#         fhead = struct.pack('128sl', bytes(os.path.basename(
#             filepath).encode('utf-8')), os.stat(filepath).st_size)
#         s.send(fhead)
#         print('client filepath: {0}'.format(filepath))
#         fp = open(filepath, 'rb')
#         while 1:
#             data = fp.read(1024)
#             if not data:
#                 print('{0} file send over...'.format(filepath))
#                 break
#             s.send(data)
#     s.close()
#     break


# if __name__ == '__main__':
#     socket_client()

# # address = ('127.0.0.1', 2567)
# # photos = ['C:/Users/Winniepopu/Desktop/享藥健康_圖片上傳/1.png']


# # def send(photos):
# #     for photo in photos[0]:
# #         print('sending {}'.format(photo))
# #         data = file_deal(photo)
# #         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #         sock.connect(address)
# #         # 默认编码 utf-8,发送文件长度和文件名
# #         sock.send('{}|{}'.format(len(data), file).encode())
# #         reply = sock.recv(1024)
# #         if 'ok' == reply.decode():  # 确认一下服务器get到文件长度和文件名数据
# #             go = 0
# #             total = len(data)
# #             while go < total:  # 发送文件
# #                 data_to_send = data[go:go + 1024]
# #                 sock.send(data_to_send)
# #                 go += len(data_to_send)
# #             reply = sock.recv(1024)
# #             if 'copy' == reply.decode():
# #                 print('{} send successfully'.format(photo))
# #         sock.close()  # 由于tcp是以流的形式传输数据，我们无法判断开头和结尾，简单的方法是没传送一个文件，就使用一个socket，但是这样是消耗计算机的资源，博主正在探索更好的方法，有机会交流一下


# # def file_deal(file_path):  # 读取文件的方法
# #     mes = b''
# #     try:
# #         file = open(file_path, 'rb')
# #         mes = file.read()
# #     except:
# #         print('error{}'.format(file_path))
# #     else:
# #         file.close()
# #         return mes


# # send(photos)
