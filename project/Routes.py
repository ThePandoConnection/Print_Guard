from werkzeug.utils import secure_filename
from project import app
from project.Arduino_serial import SerialRead
from flask import render_template, redirect, url_for, request, session, jsonify


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():

    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(filename)
        file = f.filename
        return render_template('home.html', name=file)
    return render_template("home.html")

@app.route("/stream")
def stream_temp():
    if request.method == 'GET':
        output = []
        output = SerialRead('COM4', output)
        out = output.split()
        temp = out[1]
        humi = out[2]
        if out[0] == 'Dark':
            state = 'OK'
        else:
            state = 'RUNOUT'
        status = 'Ready'
        return jsonify(temp=temp, humi=humi, state=state, status=status)