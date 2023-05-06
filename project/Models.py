from project import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f"user('{self.username}')"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
