import cv2
import dlib
import imutils
import os
import pygame
from flask import Flask, render_template, Response, jsonify
from imutils import face_utils
from utils import eye_aspect_ratio, mouth_aspect_ratio

# --- Audio Setup ---
pygame.mixer.init()
base_path = os.path.dirname(os.path.abspath(__file__))
ALARM_PATH = os.path.join(base_path, "static", "alarm.wav")
if os.path.exists(ALARM_PATH):
    pygame.mixer.music.load(ALARM_PATH)

app = Flask(__name__)

# --- Model Setup ---
model_path = os.path.join(base_path, "models", "shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(model_path)

# --- Configuration ---
EAR_THRESHOLD = 0.22  
MAR_THRESHOLD = 0.5   
EYE_LIMIT = 60  # ~3 seconds at 20fps
YAWN_LIMIT = 20 # ~1 second yawn

EYE_COUNTER = 0
YAWN_COUNTER = 0
ALARM_ON = False
DATA_LOG = {"ear": 0.3, "mar": 0.1, "alarm": False}

def generate_frames():
    global EYE_COUNTER, YAWN_COUNTER, ALARM_ON, DATA_LOG
    camera = cv2.VideoCapture(0)
    
    while True:
        success, frame = camera.read()
        if not success: break
        
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)

        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            leftEye = shape[36:42]
            rightEye = shape[42:48]
            mouth = shape[48:68]
            
            ear = (eye_aspect_ratio(leftEye) + eye_aspect_ratio(rightEye)) / 2.0
            mar = mouth_aspect_ratio(mouth)
            
            DATA_LOG["ear"] = ear
            DATA_LOG["mar"] = mar

            # Drowsiness Engine
            if ear < EAR_THRESHOLD:
                EYE_COUNTER += 1
            else:
                EYE_COUNTER = 0

            if mar > MAR_THRESHOLD:
                YAWN_COUNTER += 1
            else:
                YAWN_COUNTER = 0

            if EYE_COUNTER >= EYE_LIMIT or YAWN_COUNTER >= YAWN_LIMIT:
                DATA_LOG["alarm"] = True
                if not ALARM_ON:
                    ALARM_ON = True
                    if os.path.exists(ALARM_PATH): pygame.mixer.music.play(-1)
            else:
                DATA_LOG["alarm"] = False
                if ALARM_ON and EYE_COUNTER == 0 and YAWN_COUNTER == 0:
                    pygame.mixer.music.stop()
                    ALARM_ON = False

            # Visual Feedback
            cv2.drawContours(frame, [cv2.convexHull(leftEye)], -1, (254, 242, 0), 1)
            cv2.drawContours(frame, [cv2.convexHull(rightEye)], -1, (254, 242, 0), 1)
            cv2.drawContours(frame, [cv2.convexHull(mouth)], -1, (0, 255, 255), 1)

        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index(): return render_template('index.html')

@app.route('/video_feed')
def video_feed(): return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_data')
def get_data(): return jsonify(DATA_LOG)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)