from flask import Flask, render_template, Response, stream_with_context, request, redirect, url_for, flash
import cv2
import torch
import yt_dlp
import sys
import os

# Redirect stdout and stderr to null (or to a log file if needed)
sys.stdout = open('stdout.log', 'w')
sys.stderr = open('stderr.log', 'w')

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Hardcoded credentials
USERNAME = 'admin'
PASSWORD = 'password123'

# Function to extract the best stream URL using yt-dlp
def get_best_stream_url(url):
    ydl_opts = {
        'format': 'best',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict['url']

def detect_objects_in_frame(model, frame):
    # Perform inference on the frame
    results = model(frame)

    # Count the number of cows detected
    cow_count = 0
    for result in results.xyxy[0]:
        label = model.names[int(result[-1])]
        if "cow" in label.lower():
            cow_count += 1

    # Render the results (draw bounding boxes and labels on the frame)
    results.render()

    # Convert the frame back to BGR (OpenCV format) from RGB
    output_frame = cv2.cvtColor(results.ims[0], cv2.COLOR_RGB2BGR)
    return output_frame, cow_count

def generate_frames(stream_url):
    cap = cv2.VideoCapture(stream_url)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            detected_frame, cow_count = detect_objects_in_frame(model, frame)
            ret, buffer = cv2.imencode('.jpg', detected_frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Redirect root URL to login
@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hardcoded credential check
        if username == USERNAME and password == PASSWORD:
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/lifecycle')
def lifecycle():
    return render_template('lifecycle.html')

@app.route('/video_feed')
def video_feed():
    video_url = "https://www.youtube.com/watch?v=6PsITx_ynqQ"  # Replace with your video URL
    stream_url = get_best_stream_url(video_url)
    return Response(generate_frames(stream_url), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cow_count_feed')
def cow_count_feed():
    video_url = "https://www.youtube.com/watch?v=6PsITx_ynqQ"  # Replace with your video URL
    stream_url = get_best_stream_url(video_url)

    def generate_cow_count():
        cap = cv2.VideoCapture(stream_url)
        while True:
            success, frame = cap.read()
            if not success:
                break
            else:
                _, cow_count = detect_objects_in_frame(model, frame)
                yield f"data:{cow_count}\n\n"

    return Response(stream_with_context(generate_cow_count()), content_type='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)
