from project import app, main, fail_classifier_training
from project.Arduino_serial import SerialRead
from project.main import loadGcode, PrintThread
from flask import render_template, redirect, url_for, request, jsonify, Response, g
import os

# from Arduino_serial import SerialRead


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
        temp = 19
        humi = 50
        state = 'OK'
        #if ((temp < 20) or (humi > 50) or (state != 'OK')) and (not pause) and running:
            #error = True
        #else:
            #error = False
        status = 'Ready'

        return jsonify(temp=temp, humi=humi, state=state, status=status)


@app.route('/classify')
def classify_image():
    predicted, confidence = fail_classifier_training.get_image()
    return jsonify(predicted=predicted, confidence=confidence)


@app.route('/start_printer')
def start_print():
    f = loadGcode('print')
    g.thread = PrintThread(f, port='COM3', baudrate=115200)
    g.thread.start()
    return Response(status=200)


@app.route('/pause_printer')
def pause_print():
    g.thread.pause()
    return Response(status=200)


@app.route('/resume_printer')
def resume_print():
    g.thread.resume()
    return Response(status=200)
