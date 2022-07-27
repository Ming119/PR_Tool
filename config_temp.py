import os
from datetime import timedelta

SECRET_KEY = os.urandom(256)
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database/test.db') 
SQLALCHEMY_TRACK_MODIFICATIONS = True

GITHUB_CLIENT_ID = ""
GITHUB_CLIENT_SECRET = ""

OWNER = "sunbirddcim"
REPO  = "test_automation"
BRANCH = "9.0.0-branch"