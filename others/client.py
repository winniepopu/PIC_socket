from socket import *
import tkinter as tk
import tkinter.scrolledtext as tst
import time
import tkinter.messagebox
import threading
import requests
import io
from PIL import Image, ImageTk
# 定義輸入服務器ip地址的類


class inputIPdialog(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.ipInput = tk.Text(self, width=40, height=5)
        self.ipInput.grid(row=0, column=0, columnspan=3)
        self.okbtn = tk.Button(
            self, text='確定', command=self.setIP).grid(row=1, column=3)
        self.grid()

    def setIP(self):
        # 這個global變量作爲類變量的話沒有效果，原因不知
        global servername
        servername = self.ipInput.get('1.0', 'end-1c')
        # 銷燬窗口
        ipRootFrame.destroy()


class inputName(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.nameInput = tk.Text(self, width=30, height=5)
        self.nameInput.grid(row=0, column=0, columnspan=3)
        self.nameOkbtn = tk.Button(
            self, text='確定', command=self.setUsername).grid(row=1, column=3)
        self.name = ""
        self.grid()

    def setUsername(self):
        Name = self.nameInput.get('1.0', 'end-1c')
        print("Name:", Name)
        self.name = Name

        clientSocket.send(bytes(Name, encoding='utf8'))
        UsernameFrame.destroy()


class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.emoji = {0: "( ͡~ ͜ʖ ͡~)", 1: "( ͡ಠ ʖ̯ ͡ಠ)",
                      2: '凸(⊙▂⊙ )', 3: 'ꈍ .̮ ꈍ', 4: '(・∀・)', 5: '(　´_ゝ`)'}

    def createWidgets(self):
        self.textEdit = tst.ScrolledText(self, width=50, height=30)
        self.textEdit.grid(row=0, column=0, rowspan=1, columnspan=12, pady=5)
        # 定義標籤，改變字體顏色
        self.textEdit.tag_config('server', foreground='purple')
        self.textEdit.tag_config('guest', foreground='blue')
        self.textEdit.tag_config(
            'important', foreground='red', font=('Arial', 12, 'bold'))
        self.emoji_btn = tk.Button(
            self, text='( ͡~ ͜ʖ ͡~)', command=self.textInsert0, bg="#FFC8B4")
        self.emoji_btn.grid(row=1, column=0, padx=5)
        self.emoji_btn = tk.Button(
            self, text='( ͡ಠ ʖ̯ ͡ಠ)', command=self.textInsert1, bg="#FFC8B4")
        self.emoji_btn.grid(row=1, column=1)
        self.emoji_btn = tk.Button(
            self, text='凸(⊙▂⊙ )', command=self.textInsert2, bg="#FFC8B4")
        self.emoji_btn.grid(row=1, column=2)
        self.emoji_btn = tk.Button(
            self, text='ꈍ .̮ ꈍ', command=self.textInsert3, bg="#FFC8B4")
        self.emoji_btn.grid(row=1, column=3)
        self.emoji_btn = tk.Button(
            self, text='(・∀・)', command=self.textInsert4, bg="#FFC8B4")
        self.emoji_btn.grid(row=1, column=4)
        self.emoji_btn = tk.Button(
            self, text='(　´_ゝ`)', command=self.textInsert5, bg="#FFC8B4")
        self.emoji_btn.grid(row=1, column=5)
        # 編輯窗口
        self.inputText = tk.Text(self, width=40, height=5)
        self.inputText.grid(row=2, column=0, columnspan=6, pady=5)
        # 定義快捷鍵，按下回車即可發送消息
        self.inputText.bind("<KeyPress-Return>", self.textSendReturn)
        # 發送按鈕
        self.btnSend = tk.Button(
            self, text='send', command=self.textSend, bg="#FFC8B4")
        self.btnSend.grid(row=2, column=8)

        self.res = requests.get(
            "https://image.flaticon.com/icons/png/512/1157/1157000.png")
        # 在這個範例當中，以yahoo首頁的圖片當作範例使用

        self.imagebyte = io.BytesIO(self.res.content)
        # 將requests抓回來的圖片作串流的轉換
        self.imagepil = Image.open(self.imagebyte)
        w, h = self.imagepil.size

        self.pil_image_resized = self.resize(w, h, 20, 20, self.imagepil)
        # self.tk_image = ImageTk.PhotoImage(pil_image_resized)
        self.imagetk = ImageTk.PhotoImage(self.pil_image_resized)
        # self.imagetk = ImageTk.PhotoImage(self.imagepil)
        self.bellBtn = tk.Button(
            self, image=self.imagetk, width=20, height=20, command=self.call)
        self.bellBtn.grid(row=1, column=6)

        # 開啓一個線程用於接收消息並顯示在聊天窗口
        t = threading.Thread(target=self.getInfo)
        t.start()

    def call(self):
        sendMessage = bytes("有人在家嗎!!", encoding='utf8')
        # 發送輸入的數據，與UDP有點不同，使用的是send方法，不需要指定服務器和端口，因爲已經建立了一條tcp連接
        clientSocket.send(sendMessage)
        self.textEdit.config(state='normal')
        self.textEdit.insert(tk.END, "有人在家嗎!!\n", 'important')
        self.textEdit.see(tk.END)
        self.textEdit.config(state='disabled')

    def resize(self, w, h, w_box, h_box, pil_image):
        ''' 
        resize a pil_image object so it will fit into 
        a box of size w_box times h_box, but retain aspect ratio 
        对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例 
        '''
        f1 = 1.0*w_box/w  # 1.0 forces float division in Python2
        f2 = 1.0*h_box/h
        factor = min([f1, f2])
        # print(f1, f2, factor) # test
        # use best down-sizing filter
        width = int(w*factor)
        height = int(h*factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    def textInsert0(self):
        self.inputText.insert(tk.END, self.emoji[0])

    def textInsert1(self):
        self.inputText.insert(tk.END, self.emoji[1])

    def textInsert2(self):
        self.inputText.insert(tk.END, self.emoji[2])

    def textInsert3(self):
        self.inputText.insert(tk.END, self.emoji[3])

    def textInsert4(self):
        self.inputText.insert(tk.END, self.emoji[4])

    def textInsert5(self):
        self.inputText.insert(tk.END, self.emoji[5])

    def textSend(self):
        # 獲取Text的所有內容
        str = self.inputText.get('1.0', 'end-1c')
        if str != "" and str != None:
            # 顯示發送時間和發送消息
            timemsg = '本地端' + \
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+'\n'
            # 通過設置state屬性設置textEdit可編輯
            self.textEdit.config(state='normal')

            self.textEdit.insert(tk.INSERT, timemsg, 'guest')
            self.textEdit.insert(tk.INSERT, str+'\n')

            # 將滾動條拉到最後顯示最新消息
            self.textEdit.see(tk.END)
            # 通過設置state屬性設置textEdit不可編輯
            self.textEdit.config(state='disabled')
            self.inputText.delete(0.0, tk.END)  # 刪除輸入框的內容
            # 發送數據到服務端
            sendMessage = bytes(str, encoding='utf8')
            # 發送輸入的數據，與UDP有點不同，使用的是send方法，不需要指定服務器和端口，因爲已經建立了一條tcp連接
            clientSocket.send(sendMessage)
        else:
            tk.messagebox.showinfo('警告', "不能發送空白信息！")

    def getInfo(self):
        global clientSocket
        while True:
            # 接收數據,1024指定緩存長度，使用的是recv方法
            recMsg = clientSocket.recv(1024).decode("utf8")+'\n'
            # 接受時間和接收的數據
            recTime = '\n'+'服務端' + \
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+'\n'
            self.textEdit.config(state='normal')
            if recMsg == "有人在家嗎!!\n":
                self.textEdit.insert(tk.END, recMsg, 'important')
            else:
                self.textEdit.insert(tk.END, recTime, 'server')
                self.textEdit.insert(tk.END, recMsg+'\n')
            # server作爲標籤,改變字體顏色
            # 將滾動條拉到最後顯示最新消息
            self.textEdit.see(tk.END)
            self.textEdit.config(state='disabled')

    def textSendReturn(self, event):
        if event.keysym == "Return":
            self.textSend()


# 指定服務器地址，端口
servername = '140.116.96.107'
serverport = 12001

# ipRootFrame = tk.Tk()
# ipRootFrame.title('請輸入Server ip')
# ipDialog = inputIPdialog(ipRootFrame)
# ipDialog.mainloop()

# socket第一個參數指定使用IPV4協議，第二個參數指定這是一個TCP套接字
clientSocket = None

try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
except:
    tk.messagebox.showinfo('未知錯誤', '檢查服務器地址是否錯誤！')


# tcp連接需要先經過握手建立連接
clientSocket.connect((servername, serverport))

UsernameFrame = tk.Tk()
UsernameFrame.title('請輸入暱稱')
name = inputName(UsernameFrame)
name.mainloop()
root = tk.Tk()
root.title(name.name+"端 - 2020即時通")
app = Application(master=root)
app.configure(bg='#FFCCCC')
app.mainloop()
