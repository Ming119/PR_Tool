import base64
import threading
from flask import current_app, request, session, flash, render_template, redirect, url_for, make_response, jsonify, copy_current_request_context
from util import github, authorization_required, org_access_required, team_required

from models import TeamMember, TeamAssignee, TeamLabel, TeamReviewer

@current_app.route("/", methods=['GET', 'POST'])
@authorization_required
@org_access_required
@team_required
def index(user, team):
    kwargs = {
        "user": user,
        "team": team,
    }

    return render_template("index.html", kwargs=kwargs)

@current_app.route("/fetchPRs", methods=['GET'])
@authorization_required
@org_access_required
@team_required
def fetchPRs(user, team):
    team   = request.args.get("team")
    state  = request.args.get("state")
    
    team_members = TeamMember.getTeamMembers(team=team)
    if not team_members: return jsonify([])
    team_members_list = [team_member.user for team_member in team_members]
    
    issues = github.list_pull_requests(team_members_list, state)

    if (state == 'closed'):
        resp = [{
            'number': f"#{pr['number']}",
            'title': pr['title'],
            'date': pr['closed_at'][:10],
            'author': pr['user']['login'],
            'labels': [{
                'name': label['name'],
                'color': label['color']
            } for label in pr['labels']],
            'base_on': config.BRANCH,
            'url': pr['html_url'],
        } for pr in issues['items']]
        return jsonify(resp)
    
    issues_number = [issue['number'] for issue in issues['items']]
    
    @copy_current_request_context
    def job(issue_num):
        res = github.get_a_pull_request(issue_num)
        resp.append({
            'number': f"#{res['number']}",
            'title': res['title'],
            'date': res['created_at'][:10],
            'labels': [{
                'name': label['name'],
                'color': label['color']
            } for label in res['labels']],
            'author': res['user']['login'],
            'base_on': res['base']['ref'],
            'url': res['html_url'],
        })

    resp = []
    threads = [threading.Thread(target=job, args=(issue_number,)) for issue_number in issues_number]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return jsonify(resp)

@current_app.route("/login/oauth", methods=["GET"])
def oauth():
    if session.get("token", None):
        flash("Authorizated.", "success")
        return redirect(url_for("index"))

    return github.authorize(scope="repo")

@current_app.route("/login/authorized", methods=["GET"])
@github.authorized_handler
def authorized(access_token):
    if access_token is None:
        flash("Authorization failed.", "danger")
    else:
        session["token"] = access_token
        flash("Authorizated.", "success")

    next_url = request.args.get("next") or url_for("index")
    return redirect(next_url)

# WIP function
@current_app.route("/logout", methods=["GET"])
def logout():
    # github.logout(token)
    # res = make_response(redirect(url_for("index")))
    # session.pop("token")
    # res.set_cookie(key='session', value='', expires=0)
    # github.delete_an_app_authorization(token)
    return "WIP"

@current_app.route("/orgAccessError", methods=["GET"])
@authorization_required
def orgAccessError():
    return render_template("orgAccessError.html")

@current_app.route("/joinTeam", methods=["GET"])
@authorization_required
@org_access_required
def joinTeam(user):
    kwargs = {
        "user": user,
    }

    team = request.args.get("team")
    if not team:
        return render_template("joinTeam.html", kwargs=kwargs)
    
    if TeamMember.add(team, user):
        session["team"] = team
        flash(f"Joined {team}.", "success")
        return redirect(url_for("index"))
    flash(f"Failed to join {team}, please try again.", "danger")
    return redirect(url_for("joinTeam"))

@current_app.route("/uploadFile", methods=["GET", "POST"])
@authorization_required
@org_access_required
@team_required
def uploadFile(user, team):
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

    kwargs = {
        "user": user,
        "team": team,
    }

    return render_template("uploadFile.html", kwargs=kwargs)

@current_app.route("/newPullRequest", methods=["GET", "POST"])
@authorization_required
@org_access_required
@team_required
def newPullRequest(user, team):
    kwargs = {
        "user": user,
        "team": team,
    }

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
        
        @copy_current_request_context
        def job_request_reviewers_for_a_pull_request(reviewers):
            github.request_reviewers_for_a_pull_request(pull_number=res["number"], reviewers=reviewers)
        
        @copy_current_request_context
        def add_assignees_to_an_issue(assignees):
            github.add_assignees_to_an_issue(issue_number=res["number"], assignees=assignees)
        
        @copy_current_request_context
        def add_labels_to_an_issue(lables):
            github.add_labels_to_an_issue(issue_number=res["number"], labels=lables)

        threads = [threading.Thread(target=job_request_reviewers_for_a_pull_request, args=(reviewers,)),
                   threading.Thread(target=add_assignees_to_an_issue, args=(assignees,)),
                   threading.Thread(target=add_labels_to_an_issue, args=(lables,))]
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()

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
                        .replace('## Your one line summary goes here (additional details go at the end)\n', f'This branch is based on `{github.BRANCH}`\nWe have already run CI.\nPlease have a look.\n', 1) \
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
@authorization_required
@org_access_required
def changeLogs(user):
    kwargs = {
        "user": user,
    }
    return render_template("changeLogs.html", kwargs=kwargs)

@current_app.route("/help", methods=["GET"])
@authorization_required
@org_access_required
def help(user):
    kwargs = {
        "user": user,
    }
    return render_template("help.html", kwargs=kwargs)
