from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

app = Flask(__name__)
app.secret_key = '2ab13a2591328f4642328cb87ebced14e22d51353684e7a8'
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1949524:Mfl9(ZFrmckEAMJ*@csmysql.cs.cf.ac.uk:3306/c1949524_cmt120_practice'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
