from project import db, login_manager
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    username=db.Column(db.String(15),unique=True,nullable=False)
    def __repr__(self):
        return f"User('{self.username}')"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
