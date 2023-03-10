from flask_login import UserMixin,login_user,login_required,logout_user,LoginManager,current_user
from datetime import datetime
from __init__ import db
import enum, re, random, pytz
from sqlalchemy.orm import backref
tz = pytz.timezone('Africa/Nairobi')

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(80),unique=True)
    username = db.Column(db.String(80),unique=True)
    pwd = db.Column(db.String(300), nullable=False, unique=True)
    authenticated = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    # def is_active(self):
    #     return True

    # def get_id(self):
    #     return self.email

    # def is_authenticated(self):
    #     return self.authenticated

    # def is_anonymous(self):
    #     return False