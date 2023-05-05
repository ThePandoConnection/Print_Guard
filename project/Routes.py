from project import app, main, fail_classifier_training
from project.Arduino_serial import SerialRead
from project.main import loadGcode, PrintThread
from flask import render_template, redirect, url_for, request, jsonify, Response, g
import os

# from Arduino_serial import SerialRead
thread = None

@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        f = request.files['file']
        f.save('print.gcode')
        f.close()

    return render_template("home.html")


@app.route("/stream")
def stream():
    if request.method == 'GET':
        # output = SerialRead('COM4')
        # output.split()
        # print(output)
        temp = 20
        humi = 50
        state = 'OK'
        finished = False
        try:
            if thread.is_alive():
                status = 'Printing'
            else:
                status = 'Ready'
                finished = True
            if (temp < 20) or (humi > 50) or (state != 'OK') and thread.is_alive():
                print('here')
                error = True
            else:
                error = False
        except AttributeError:
            status = 'Ready'
            error = False
            finished = False

        return jsonify(temp=temp, humi=humi, state=state, status=status, error=error, finished=finished)


@app.route('/classify')
def classify_image():
    predicted, confidence = fail_classifier_training.get_image()
    return jsonify(predicted=predicted, confidence=confidence)


@app.route('/start_printer')
def start_print():
    global thread
    f = loadGcode('print')
    thread = PrintThread(f, port='COM3', baudrate=115200)
    thread.start()
    return Response(status=200)


@app.route('/pause_printer')
def pause_print():
    thread.pause()
    return Response(status=200)


@app.route('/resume_printer')
def resume_print():
    thread.resume()
    return Response(status=200)
