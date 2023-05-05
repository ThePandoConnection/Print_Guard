from werkzeug.utils import secure_filename
from project import app, login_manager
from project.Models import User
from project.Forms import LoginForm
from project.Arduino_serial import SerialRead
from flask import render_template, redirect, url_for, request, session, jsonify,flash
from flask_login import login_user, logout_user, current_user
import html


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():
    #if current_user.is_authenticated:
    return render_template("index.html")
    #else:
        #return redirect(url_for('login'))

@app.route("/stream")
def stream_temp():
    if request.method == 'GET':
        temp = 20
        humi = 50
        state = 'OK'
        status = 'Ready'
        return jsonify(temp=temp, humi=humi, state=state, status=status)

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
