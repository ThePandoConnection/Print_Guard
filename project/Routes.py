import serial.serialutil
import requests
from werkzeug.utils import secure_filename
from project import app, login_manager, fail_classifier_training, db
from project.Models import User
from project.Forms import RegistrationForm, LoginForm
from project.Arduino_serial import SerialRead, SerialWrite
from flask_login import login_user, logout_user, current_user
import html
import cv2
import numpy as np

from project.main import loadGcode, PrintThread
from flask import render_template, redirect, url_for, request, jsonify, Response, flash, stream_with_context

thread = None


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        f = request.files['file']
        f.save('print.gcode')
        f.close()

    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username_new.data, password=form.password_new.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        # user =  User.query.filter_by(username=form.username.data).first()
        # if user is not None and True: #user.verify_password(form.password.data)
        #  login_user(user)
        # flash(html.escape(current_user.username) +' Logged in')
        return redirect(url_for('home'))
    # flash('Incorrect username or password combination.')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('login'))


def gen_frames():
    url = 'http://192.168.0.210/stream'
    while True:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Read the response data and convert it to a NumPy array
            data = b""
            for chunk in response.iter_content(chunk_size=1024):
                data += chunk
                a = data.find(b"\xff\xd8")
                b = data.find(b"\xff\xd9")
                if a != -1 and b != -1:
                    jpg = data[a:b + 2]
                    data = data[b + 2:]
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    cv2.imwrite('./camera/image.jpg', frame)

                    # Convert the OpenCV frame to a byte string
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()

                    # Yield the byte string as a Flask response
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            # If the response status code is not 200, break the loop
            break


@app.route('/stream_url')
def stream_url():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/stream")
def stream():
    if request.method == 'GET':
        try:
            output = SerialRead('COM6')
            out = output.split()
            if out[0] == 'Light':
                state = '!OK'
            else:
                state = 'RUNOUT!'
            temp = out[1]
            humi = out[2]
            finished = False
            try:
                if thread.is_alive():
                    status = 'Printing'
                else:
                    status = 'Ready'
                    finished = True
                if ((float(temp) < 20) or (float(humi) > 50) or (state != 'OK')) and (
                        thread.is_alive() and (not thread.isPaused())):
                    error = True
                    SerialWrite('COM6')
                else:
                    error = False
            except AttributeError:
                status = 'Ready'
                error = False
                finished = False
        except serial.serialutil.SerialException:
            temp = 20
            humi = 50
            state = 'OK'
            status = 'Unknown'
            error = False
            finished = False

        return jsonify(temp=temp, humi=humi, state=state, status=status, error=error, finished=finished)


@app.route('/classify')
def classify_image():
    predicted, confidence = fail_classifier_training.classifyImage('flask')
    return jsonify(predicted=predicted, confidence=confidence)


@app.route('/start_printer')
def start_print():
    global thread
    try:
        f = loadGcode('print')
        thread = PrintThread(f, port='COM3', baudrate=115200)
        thread.start()
    except FileNotFoundError:
        flash('Please upload a file first')

    return Response(status=200)


@app.route('/pause_printer')
def pause_print():
    thread.pause()
    return Response(status=200)


@app.route('/resume_printer')
def resume_print():
    thread.resume()
    return Response(status=200)
