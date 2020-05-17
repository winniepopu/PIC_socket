# PIC_socket
一個有GUI介面，幫助截圖、開啟資料夾、傳送圖片的小工具

## 功能
- 擷圖
- 開啟圖片資料夾
- 利用socket傳送圖片

## socket 前置作業
到pic_taker.py 的 fun sendingPics():
更改server IP位置
```
def sendingPics():
    host = '{server IP}'  # 對server端為主機位置
    port = 5555
    address = (host, port)
```
