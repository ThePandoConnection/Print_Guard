import serial.serialutil
from werkzeug.utils import secure_filename
from project import app, login_manager, fail_classifier_training
from project.Models import User
from project.Forms import LoginForm
from project.Arduino_serial import SerialRead, SerialWrite
from flask_login import login_user, logout_user, current_user
import html

from project.main import loadGcode, PrintThread
from flask import render_template, redirect, url_for, request, jsonify, Response, flash

thread = None


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        f = request.files['file']
        f.save('print.gcode')
        f.close()

    return render_template("index.html")


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
                if ((float(temp) < 20) or (float(humi) > 50) or (state != 'OK')) and (thread.is_alive() and (not thread.isPaused())):
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
    predicted, confidence = fail_classifier_training.classifyImage()
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
