import struct
import socket
import subprocess
import tkinter as tk
import time
import win32gui
import win32ui
import win32con
import win32api
import time
import os

SaveDirectory = os.getcwd()  # 印出目前工作目錄
# SaveAs = os.path.join(SaveDirectory,'ScreenShot_' + time.strftime('%Y_%m_%d_%H_%M_%S') + '.jpg')#組合路徑，自動加上兩條斜線 "\\"
PATH = os.getcwd() + "\\pics\\"


def window_capture():
    window.withdraw()
    time.sleep(0.2)

    now_time = time.strftime("%y%m%d%H%M%S", time.localtime())

    if not os.path.isdir(PATH):
        os.mkdir(PATH)

    filename = os.path.join(PATH, "pic_"+now_time+".jpg")

    # filename = os.path.join(path,filename)

    # file = open(path + "\\" + "我要開檔案.txt", "w")

    hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片

    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)
    window.wm_deiconify()


# beg = time.time()
# for i in range(10):
#     window_capture("haha.jpg")
# end = time.time()
# print(end - beg)


def openDir():
    print(PATH)
    # C:\Users\winniepopu\Desktop\享藥健康_pic\pics
    # subprocess.Popen(r'explorer "C:\Users\winniepopu\Desktop\享藥健康_pic\pics"')
    subprocess.Popen('explorer "' + PATH+'"')


def get_filelist(PATH):
    # PATH = os.getcwd() + "\\pics"
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


# root = Tk()
window = tk.Tk()
window.wm_attributes('-topmost', 1)
window.title('PIC taker')
window.geometry('190x135')

window.configure(background='white')


PrtSc_btn = tk.Button(
    window, width=25, height=2, text='進行截圖', command=window_capture)
PrtSc_btn.pack()


OpenDir_btn = tk.Button(
    window, width=25, height=2, text='開啟截圖資料夾', command=openDir)
OpenDir_btn.pack()

Upload_btn = tk.Button(
    window, width=25, height=2, text='上傳所有圖片', command=sendingPics)
Upload_btn.pack()


window.mainloop()


# header_label = tk.Label(window, text='BMI 計算器')
# header_label.pack()

# # 以下為 height_frame 群組
# height_frame = tk.Frame(window)
# # 向上對齊父元件
# height_frame.pack(side=tk.TOP)
# height_label = tk.Label(height_frame, text='身高（m）')
# height_label.pack(side=tk.LEFT)
# height_entry = tk.Entry(height_frame)
# height_entry.pack(side=tk.LEFT)

# # 以下為 weight_frame 群組
# weight_frame = tk.Frame(window)
# weight_frame.pack(side=tk.TOP)
# weight_label = tk.Label(weight_frame, text='體重（kg）')
# weight_label.pack(side=tk.LEFT)
# weight_entry = tk.Entry(weight_frame)
# weight_entry.pack(side=tk.LEFT)

# result_label = tk.Label(window)
# result_label.pack()
