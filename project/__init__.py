from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '2ab13a2591328f4642328cb87ebced14e22d51353684e7a8'
app.debug = True

from project import Routes