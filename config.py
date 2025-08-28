# Handles configurations
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Database configurations
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key-here'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATION = False
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
