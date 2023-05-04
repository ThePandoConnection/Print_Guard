from werkzeug.utils import secure_filename
from project import app, main
from project.Arduino_serial import SerialRead
from project.main import loadGcode, PrintThread
from flask import render_template, redirect, url_for, request, session, jsonify, Response
import os

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
        #output = SerialRead('COM4')
        #output.split()
        #print(output)
        temp = 20
        humi = 50
        state = 'OK'
        status = 'Ready'
        return jsonify(temp=temp, humi=humi, state=state, status=status)


@app.route('/start_printer')
def start_print():
    f = loadGcode('print')
    thread = PrintThread(f, port='COM3', baudrate=115200)
    thread.start()

    return Response(status=200)

@app.route('/pause_printer')
def pause_print():
    main.pause = True
    return Response(status=200)

@app.route('/resume_printer')
def resume_print():
    main.pause = False
    return Response(status=200)
