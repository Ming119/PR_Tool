from flask import current_app, session
from flask_sqlalchemy import SQLAlchemy
from GitHubApi import GitHubApi

db = SQLAlchemy(current_app)
github = GitHubApi(current_app)

@github.access_token_getter
def token_getter():
    token = session.get("token", None)
    if token is not None:
        return token

def init_db():
    # db.drop_all()
    # db.create_all()
    return
