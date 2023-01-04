from flask import Flask, render_template, Response
import cv2
import numpy as np
import nxt_call

app = Flask(__name__)


def gen_frames():
    CAMERA_DEVICE_ID = 0
    IMAGE_WIDTH = 640
    IMAGE_HEIGHT = 480
    detected = False
    wait = 0
    try:
        # create video capture
        cap = cv2.VideoCapture(CAMERA_DEVICE_ID)

        # 設定擷取影像的尺寸大小
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)

        # 初始化平均影像
        ret, frame = cap.read()
        avg = cv2.blur(frame, (4, 4))
        avg_float = np.float32(avg)
        # Loop to continuously get images
        while True:
            # 讀取一幅影格
            ret, frame = cap.read()
            original = frame

            # 若讀取至影片結尾，則跳出
            if ret == False:
                break

            # 模糊處理
            blur = cv2.blur(frame, (4, 4))

            # 計算目前影格與平均影像的差異值
            diff = cv2.absdiff(avg, blur)

            # 將圖片轉為灰階
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

            # 篩選出變動程度大於門檻值的區域
            ret, thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)

            # 使用型態轉換函數去除雜訊
            kernel = np.ones((5, 5), np.uint8)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

            # 產生等高線
            cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in cnts:
                # 忽略太小的區域
                if cv2.contourArea(c) < 2500:
                    continue

                # 偵測到物體，可以自己加上處理的程式碼在這裡...

                # 計算等高線的外框範圍
                (x, y, w, h) = cv2.boundingRect(c)

                # 畫出外框
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # nxt_call.call()


            # 畫出等高線（除錯用）
            # cv2.drawContours(frame, cnts, -1, (0, 255, 255), 2)

            if detected:
                cv2.imwrite('capture.jpg', original)
                nxt_call.call()
                cap.release()


            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            # 更新平均影像
            cv2.accumulateWeighted(blur, avg_float, 0.001)
            avg = cv2.convertScaleAbs(avg_float)

            if len(cnts) > 0 and wait > 50:
                detected = True

            wait += 1
            # if key pressed is 'Esc' then exit the loop
            if cv2.waitKey(33) == 27:
                break
    except Exception as e:
        print(e)
    finally:
        # Clean up and exit the program
        cv2.destroyAllWindows()
        cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('watchDog.html')

if __name__ == '__main__':
    app.run('0.0.0.0')
