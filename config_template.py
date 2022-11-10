import os
from datetime import timedelta

SECRET_KEY = os.urandom(256)
PERMANENT_SESSION_LIFETIME = timedelta(days=1)
PRESERVE_CONTEXT_ON_EXCEPTION = False

# "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database/db.sql')
SQLALCHEMY_DATABASE_URI = ""
SQLALCHEMY_TRACK_MODIFICATIONS = True

GITHUB_CLIENT_ID = ""
GITHUB_CLIENT_SECRET = ""

OWNER  = "sunbirddcim"
REPO   = "test_automation"
BRANCH = "9.1.0-branch"