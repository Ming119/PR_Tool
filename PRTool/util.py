from functools import wraps, lru_cache
from flask import current_app, session, redirect, url_for
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

def authorization_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("token", None):
            return func(*args, user=github.current_user(), **kwargs)
        return redirect(url_for("oauth"))
    return wrapper

def org_access_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasOrgAccess():
            return func(*args, **kwargs)
        return redirect(url_for("orgAccessError"))
    return wrapper

def team_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from models import TeamMember

        if session.get("team", None):
            return func(*args, team=session.get("team"), **kwargs)

        user = TeamMember.getTeamMembers(github.current_user())
        if user and user.team:
            return func(*args, team=user.team, **kwargs)

        return redirect(url_for("joinTeam"))
    return wrapper

@lru_cache()
def hasOrgAccess():
    import requests
    from config import OWNER

    headers = {
        "Authorization": f"Bearer {session.get('token', None)}",
        "Accept": "application/vnd.github+json"
    }
    
    response = requests.get(
        f"https://api.github.com/user/memberships/orgs/{OWNER}",
        headers=headers
    )

    if response.status_code == 200:
        return True
    else:
        return False
