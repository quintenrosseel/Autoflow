#import numpy as np
import cv2
from flask import Flask, render_template, Response

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.calibrate()
    def __del__(self):
        self.video.release()
    def get_frame(self):
        success, image = self.video.read()
        #image = cv2.subtract(self.base, image, -1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (11, 11), 0)
        # threshold the image to reveal light regions in the
        # blurred image
        thresh = cv2.threshold(blurred, 230, 255, cv2.THRESH_BINARY)[1]
        #thresh = cv2.adaptiveThreshold(blurred, 255, \
        #         cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        # perform a series of erosions and dilations to remove
        # any small blobs of noise from the thresholded image
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=4)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        ret, jpeg = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 20])
        return jpeg.tostring() #tostring = tobytes
    def calibrate(self):
        success, image = self.video.read()
        #ret, jpeg = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 20])
        self.base = image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\n'
               b'Content-Type: image/jpeg\n\n' + frame + b'\n')
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host='0.0.0.0')

#cap = cv2.VideoCapture(0)

#while(True):
#    ret, frame = cap.read()
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#    cv2.imshow('frame', gray)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break

#cap.release()
#cv2.destroyAllWindows()
