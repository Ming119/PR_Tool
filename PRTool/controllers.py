import base64
import json
import threading
from collections import defaultdict
from flask import current_app, request, session, flash, render_template, redirect, url_for, make_response, jsonify, copy_current_request_context
from util import github

from models import TeamMember, TeamAssignee, TeamLabel, TeamReviewer

@current_app.route("/", methods=['GET', 'POST'])
def index():
    if session.get("token", None) is None:
        return redirect(url_for("login"))

    kwargs = defaultdict(list)
    kwargs["user"] = github.current_user()
    team_members = TeamMember.getTeamMembers(kwargs.get("user"))
    if team_members: kwargs["team"] = team_members.team

    return render_template("index.html", kwargs=kwargs)

@current_app.route("/fetchPRs", methods=['GET'])
def fetchPRs():
    if session.get("token", None) is None:
        return redirect(url_for("login"))
    
    team   = request.args.get("team")
    state  = request.args.get("state")
    search = request.args.get("search")

    if ('Capstone' in team):
        team = team[0:-1] + " " + team[-1]
    
    team_members = TeamMember.getTeamMembers(team=team)
    if not team_members: return jsonify({'total_count': 0})
    team_members_list = [team_member.user for team_member in team_members]
    
    issues = github.list_pull_requests(team_members_list, state, search=search)

    if (state == 'closed'):
        resp = sorted(issues['items'], key=lambda x: x['closed_at'], reverse=True)
        return jsonify(resp)
    
    issues_number = [issue['number'] for issue in issues['items']]
    
    @copy_current_request_context
    def job(issue_num):
        resp.append(github.get_a_pull_request(issue_num))

    resp = []
    threads = [threading.Thread(target=job, args=(issue_number,)) for issue_number in issues_number]

    for i in range(len(issues_number)):
        threads[i].start()
    for i in range(len(issues_number)):
        threads[i].join()

    resp = sorted(resp, key=lambda x: x['created_at'], reverse=True)
    return jsonify(resp)


@current_app.route("/login", methods=["GET"])
def login():
    if session.get("token", None):
        flash("Authorizated.", "success")
        return redirect(url_for("index"))

    return github.authorize(scope="repo")

@current_app.route("/login/authorized", methods=["GET"])
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get("next") or url_for("index")
    if access_token is None:
        flash("Authorization failed.", "danger")

    else:
        session["token"] = access_token
        flash("Authorizated.", "success")

    return redirect(next_url)

@current_app.route("/logout", methods=["GET"])
def logout():
    # github.logout(session["token"])
    res = make_response(redirect(url_for("index")))
    session.pop("token")
    res.set_cookie(key='session', value='', expires=0)
    return res

@current_app.route("/joinTeam/<team>", methods=["GET"])
def joinTeam(team):
    if session.get("token", None) is None:
        return redirect(url_for("login"))

    TeamMember.add(team, github.current_user())

    flash(f"Joined {team}.", "success")

    return redirect(url_for("index"))

@current_app.route("/uploadFile", methods=["GET", "POST"])
def uploadFile():
    if session.get("token", None) is None:
        return redirect(url_for("login"))

    if TeamMember.getTeamMembers(github.current_user()) is None:
        flash("You have not join any team yet.", "warning")
        redirect(url_for("index"))

    # FIXME: 500 error if branch is not exist
    if request.method == "POST":
        file = request.files["file"]
        if file and github.get_a_branch(file.filename.replace(".txt", "")):
            session["fileName"] = file.filename
            session["fileContent"] = file.read().decode("utf-8")

            return redirect(url_for("newPullRequest"))

    kwargs = defaultdict(list)
    kwargs["user"] = github.current_user()
    team_members = TeamMember.getTeamMembers(kwargs.get("user"))
    if team_members: kwargs["team"] = team_members.team

    return render_template("uploadFile.html", kwargs=kwargs)

@current_app.route("/newPullRequest", methods=["GET", "POST"])
def newPullRequest():
    if session.get("token", None) is None:
        return redirect(url_for("login"))

    if TeamMember.getTeamMembers(github.current_user()) is None:
        flash("You have not join any team yet.", "warning")
        redirect(url_for("index"))

    kwargs = defaultdict(list)
    kwargs["user"] = github.current_user()
    team_members = TeamMember.getTeamMembers(kwargs.get("user"))
    if team_members: kwargs["team"] = team_members.team

    if request.method == "POST":
        base = request.form.get('base')
        head = session.get("fileName").replace(".txt", "")
        title = request.form.get('title')
        body = request.form.get('body')
        reviewers = request.form.getlist('reviewers')
        assignees = request.form.getlist('assignees')
        lables = request.form.getlist('labels')

        TeamReviewer.clean(kwargs["team"])
        TeamAssignee.clean(kwargs["team"])
        TeamLabel.clean(kwargs["team"])

        TeamReviewer.add(kwargs["team"], reviewers)
        TeamAssignee.add(kwargs["team"], assignees)
        TeamLabel.add(kwargs["team"], lables)

        res = github.create_a_pull_request(base=base, head=head, title=title, body=body)
        github.request_reviewers_for_a_pull_request(pull_number=res["number"], reviewers=reviewers)
        github.add_assignees_to_an_issue(issue_number=res["number"], assignees=assignees)
        github.add_labels_to_an_issue(issue_number=res["number"], labels=lables)

        return redirect(url_for("index"))

    template = github.get_repository_content("pull_request_template.md")

    page = 1
    while True:
        branches = github.list_branches(per_page=100, page=page)
        for branch in branches:
            kwargs["branches"].append(branch)
        if len(branches) < 100: break
        page += 1

    page = 1
    while True:
        members = github.list_organization_members(per_page=100, page=page)
        for member in members:
            kwargs["members"].append(member)
        if len(members) < 100: break
        page += 1
    
    kwargs["allLabels"] = github.list_label()

    kwargs["title"] = session.get("fileName").replace(".txt", "")
    kwargs["body"] = base64.b64decode(template.get("content")) \
                        .decode('utf-8') \
                        .replace('## Your one line summary goes here (additional details go at the end)\n', f'This branch is based on {github.BRANCH}\nWe have already run CI.\nPlease have a look.\n', 1) \
                        .replace('- [ ]', '- [x]') \
                        .replace('If this is a relatively large or complex change, please explain why you chose the solution you did and what alternatives you considered.\n', '', 1) \
                        .replace('\n', '&#13;&#10;') \
                    + session.get('fileContent').replace('\r\n', '&#13;&#10;')

    teamReviewers = TeamReviewer.getTeamReviewers(kwargs.get("team"))
    teamAssignees = TeamAssignee.getTeamAssignees(kwargs.get("team"))
    teamLabels    = TeamLabel.getTeamLabels(kwargs.get("team"))

    for teamReviewer in teamReviewers:
        kwargs["reviewers"].append(teamReviewer.reviewer)

    for teamAssignee in teamAssignees:
        kwargs["assignees"].append(teamAssignee.assignee)

    for teamLabel in teamLabels:
        kwargs["labels"].append(teamLabel.label)

    return render_template("newPullRequest.html", kwargs=kwargs)

@current_app.route("/changeLogs", methods=["GET"])
def changeLogs():
    if session.get("token", None) is None:
        return redirect(url_for("login"))

    kwargs = defaultdict(list)
    kwargs["user"] = github.current_user()
    team_members = TeamMember.getTeamMembers(kwargs.get("user"))
    if team_members: kwargs["team"] = team_members.team

    return render_template("changeLogs.html", kwargs=kwargs)

@current_app.route("/help", method=["GET"])
def help():
    if session.get("token", None) is None:
        return redirect(url_for("login"))

    kwargs = defaultdict(list)
    kwargs["user"] = github.current_user()
    team_members = TeamMember.getTeamMembers(kwargs.get("user"))
    if team_members: kwargs["team"] = team_members.team

    return render_template("help.html", kwargs=kwargs)
    