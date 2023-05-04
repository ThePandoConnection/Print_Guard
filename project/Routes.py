from werkzeug.utils import secure_filename
from project import app
from project.Arduino_serial import SerialRead
from flask import render_template, redirect, url_for, request, session, jsonify


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template("home.html")

@app.route("/stream")
def stream_temp():
    if request.method == 'GET':
        output = SerialRead('COM4')
        output.split()
        print(output)
        temp = 20
        humi = 50
        state = 'OK'
        status = 'Ready'
        return jsonify(temp=temp, humi=humi, state=state, status=status)