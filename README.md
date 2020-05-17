# PIC_socket
一個有GUI介面，幫助截圖、開啟資料夾、傳送圖片的小工具

## 功能
- 擷圖
- 開啟圖片資料夾
- 利用socket傳送圖片

## socket 前置作業
1. 到 server/pic_server.py 更改server IP位置
```
host = '{server IP}'  # 對server端為主機位置
port = 5555
address = (host, port)
```


2. 到 client/pic_client.py 的 fun sendingPics():
更改server IP位置
```
def sendingPics():
    host = '{server IP}'  # 對server端為主機位置
    port = 5555
    address = (host, port)
```


## RUN
1. 於伺服器端電腦，進入server資料夾，執行 pic_server.py
2. 再於用戶端電腦，進入client資料夾 ，執行 pic_client.py
