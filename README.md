# 111LSA-第六組-瘋狂看門狗 Crazy Watch Dog-README

## ppt連結
- https://www.canva.com/design/DAFWoibUPZs/bkghll5kDm6ulb2HZlNdxw/view?utm_content=DAFWoibUPZs&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink

## 動機發想 Motivation

- 阿棟常常帶女朋友回家住，但有時會被安同學闖入房間，因此他想了想決定在房間外養一隻看門狗，殊不知養狗的計畫還沒開始就被兇巴巴的房東阻止了，他既失望又無奈......
- 靈機一動的阿棟決定用樹莓派連接NXT機器人在門口做一隻看門狗，透過webcam觀察四周的狀況，只要安同學一靠近，就派出看門狗去扁安同學，就算安同學想逃跑也要追著她打。

## 功能 Function
- 當偵測到門外有可疑人士移動，會擷取一張即時影像，讓屋主知道要被狗追著打的人是誰
- 機器狗可以追著入侵者進行攻擊
## 樹莓派軟體使用技術
### 影像部分
- 利用OpenCV-Python 進行影像處理
- 影像會經過模糊化、灰階化，計算與前一幅影像的差異
- 高於門檻值該幅影像則偵測出有動靜
- 有動靜之區域產生等高線
- 將等高線部分匡起來
- 捨棄框太小的部分
### 網頁部分
- 在Python使用Flask架構，搭配html完成互動式介面
## 使用設備 Equiptment
- Rasberry Pi *1 (from TA NT$ 0)
- NXT *2 & LEGO零件 (一台扮演看門狗，一台為入侵者 from 晏誠 NT$ 0)
- WebCam *1 (from 順發 NT$ 699)
- SD卡 *1(from 順發 NT$169)
<!-- e.g., How many Raspberry Pi? How much you spent on these resources? -->


## 需下載項目 Installation on Raspberry Pi
- python相關

``` sudo apt install python3 ```

``` sudo apt install python3-pip ```

``` sudo apt install python3-bluez ```

``` sudo pip install nxt-python ```
- OpenCV相關

``` sudo apt install libopencv-dev ```

``` sudo apt install libatlas-base-dev ```

``` sudo pip3 install opencv-python opencv-contrib-python ```

- 網頁架構相關

``` sudo pip install flask ```

## 軟體設定 Software Setting
### NXT Programming
- 安裝 [LEGO MINDSTORMS Educate NXT programming](https://education.lego.com/en-us/downloads/retiredproducts/nxt/software)
- 使用 NXT programming 設計程式以控制機器狗
- 先自轉，利用超音波偵測敵人距離，找到敵人後貼近敵人，與敵人貼近後，在進行攻擊。
 ![](https://i.imgur.com/TDVJ6Nb.jpg)

 ![](https://i.imgur.com/qoGWh0v.jpg)

### OpenCV Setting
- 將專案下載下來 Clone

``` git clone https://github.com/JellyL1027/Watchdog.git ```
- 請先接上攝像頭 Plug Webcam in 
- 測試 Testing
``` python3 /camera-test/camera-test.py ```

### Modify Software
- cd to project folder
``` cd /Watchdog/web_watchDog ```
- 新建資料夾 static 放置圖片 Create "static" Dir
 ``` mkdir static ```
- 修改存圖片路徑
``` vim cam.py ```
- On line 76 （請使用pwd 確認static 路徑 圖檔名稱設置為capture.jpg）
```python
cv2.imwrite('/Watchdog/web_watchDog/static/capture.jpg', original)
```
- 存檔 Save

### 執行 run 
:::danger
請記得樹莓派與互動電腦要先連上同一個網域 並連接NXT與Webcam 再進行以下操作
:::
- 執行 
``` sudo python3 cam.py ```
- Terminal會跳出網址，即當下樹莓派的ip位址，如圖示
![](https://i.imgur.com/PCr6iNE.png)
- 於瀏覽器輸入 http://[ip位址]:5000

### 操作說明 
![](https://i.imgur.com/EuJoX98.png)
- 按下開始偵測按鈕即可開始偵測
- 等待一段時間即開始偵測
- 如偵測到有動靜會顯示綠框及暫停影像，瘋狂看門狗會進行攻擊 並擷取圖片，如圖示
![](https://i.imgur.com/mzLikaf.jpg)
- 如果按下顯示偵測結果按鈕，則會顯示上次偵測到的結果
- 偵測結束如需重新偵測請先 Refresh 網頁
## 硬體組裝
- 組裝兩台機器人，一台用來當作入侵者，一台當做看門狗
- 入侵者使用App遙控，機器狗藉由程式控制
- 看門狗![](https://i.imgur.com/WYHSIq9.jpg)
- 入侵者![](https://i.imgur.com/OvVAxJx.jpg)
- NXT主機![](https://i.imgur.com/VTdI96W.jpg)


## 困難及未來展望
### 困難
- 網頁架構 Flask 使用上較不習慣，需要再多精進
- 樹梅派利用藍芽連接NXT速度過慢，導致webcam也跟著當機
### 未來展望
- 網頁需要重整才能重新開啟攝像頭，希望能再多加改進，新增一個按鈕可以讓他自動重跑，無需重整頁面
- 希望能利用圖片做出更多應用（例如：將入侵者照片利用SMTP 發送郵件給主人）

## 工作分配 Job Assignment
- 109213011 張晏誠
    - 組裝NXT機器人
    - NXT programming
- 109213017 吳梓睿 
    - 影像偵測
    - 網頁對接
    - 樹莓派指令處理 
- 109213041 林國棟
    - 樹莓派利用藍芽連結NXT
    - 網頁製作 
- 109213056 趙子安 
    - 製作PPT
    - 網頁製作
- 109213058 傅裕成 
    - 製作PPT
    - 網頁製作

## 參考資料 Reference

- [Object Motion Detect](https://blog.gtwang.org/programming/opencv-motion-detection-and-tracking-tutorial/)
- [NXT Python Document](https://ni.srht.site/nxt-python/latest/index.html)
- [OpenCV test](https://github.com/automaticdai/rpi-object-detection#41-install-the-environment-on-raspberry-pi)
-  [Flask Reference -1](https://shengyu7697.github.io/python-flask-camera-streaming/)

