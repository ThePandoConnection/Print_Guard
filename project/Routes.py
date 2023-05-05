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

@app.route("/login",methods=['GET','POST'])
def login():
  form = LoginForm()
  error=None
  if form.validate_on_submit():
    #user =  User.query.filter_by(username=form.username.data).first()
    #if user is not None and True: #user.verify_password(form.password.data)
    #  login_user(user)
     #flash(html.escape(current_user.username) +' Logged in')
     return redirect(url_for('home'))
    #flash('Incorrect username or password combination.')
  return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('login'))


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
