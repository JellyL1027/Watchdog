from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)


def gen_frames():
    CAMERA_DEVICE_ID = 0
    IMAGE_WIDTH = 320
    IMAGE_HEIGHT = 240
    try:
        # create video capture
        cap = cv2.VideoCapture(CAMERA_DEVICE_ID)

        # set resolution to 320x240 to reduce latency 
        cap.set(3, IMAGE_WIDTH)
        cap.set(4, IMAGE_HEIGHT)

        # Loop to continuously get images
        while True:
            # Read the frames from a camera
            _, frame = cap.read()
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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