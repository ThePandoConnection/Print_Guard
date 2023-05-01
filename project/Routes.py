from project import app
from flask import render_template, redirect, url_for, request, session

@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template("home.html")
