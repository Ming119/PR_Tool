from typing_extensions import Self
from flask_github import GitHub
import config

class GitHubApi(GitHub):
    OWNER:  str = config.OWNER
    REPO:   str = config.REPO
    BRANCH: str = config.BRANCH

    def __init__(self, app=None):
        self.app = app
        super().__init__(app)

    def logout(self, access_token):
        return self.delete(f"/authorizations/{access_token}")

    def current_user(self):
        return self.get("user")["login"]

    def list_pull_requests(self, authors:list, state:str, per_page:int=30, page:int=1):
        query = f"/search/issues?q=repo:{self.OWNER}/{self.REPO}+state:{state}+type:pr"
        for author in authors:
            query += f"+author:{author}"
        if state == 'closed':
            query += '&sort=updated'
        return self.get(query)

    def list_opened_pull_requests(self, authors:list, sort:str="created", order:str="desc", per_page:int=30, page:int=1):
        query = f"/search/issues?sort={sort}&order={order}&per_page={per_page}&page={page}&q=repo:{self.OWNER}/{self.REPO}+state:open+type:pr"
        for author in authors:
            query += f"+author:{author}"
        return self.get(query)

    def list_closed_pull_requests(self, authors:list, sort:str="updated", order:str="desc", per_page:int=30, page:int=1):
        query = f"/search/issues?sort={sort}&order={order}&per_page={per_page}&page={page}&q=repo:{self.OWNER}/{self.REPO}+state:closed+type:pr"
        for author in authors:
            query += f"+author:{author}"
        return self.get(query)

    def create_a_pull_request(self, head:str, base:str, title:str, body:str):
        return self.post(f"/repos/{self.OWNER}/{self.REPO}/pulls", data={
            "head":  head,
            "base":  base,
            "title": title,
            "body":  body
        })

    def request_reviewers_for_a_pull_request(self, pull_number:int, reviewers:list):
        return self.post(f"/repos/{self.OWNER}/{self.REPO}/pulls/{pull_number}/requested_reviewers", data={
            "reviewers": reviewers 
        })

    def add_assignees_to_an_issue(self, issue_number:int, assignees:list):
        return self.post(f"/repos/{self.OWNER}/{self.REPO}/issues/{issue_number}/assignees", data={
            "assignees": assignees
        })
    
    def add_labels_to_an_issue(self, issue_number:int, labels:list):
        return self.post(f"/repos/{self.OWNER}/{self.REPO}/issues/{issue_number}/labels", data={
            "labels": labels
        })

    def get_repository_content(self, path:str, branch:str=''):
        return self.get(f"repos/{self.OWNER}/{self.REPO}/contents/{path}", params={
                "ref": branch or self.BRANCH
            })

    def list_branches(self, per_page:int=30, page:int=1):
        return self.get(f"repos/{self.OWNER}/{self.REPO}/branches", params={
                "per_page": per_page,
                "page": page
            })

    def get_a_branch(self, branch:str):
        return self.get(f"repos/{self.OWNER}/{self.REPO}/branches/{branch}")

    def list_organization_members(self, filter:str="all", role:str="all", per_page:int=30, page:int=1):
        return self.get(f"orgs/{self.OWNER}/members", params={
                "filter": filter,
                "role": role,
                "per_page": per_page,
                "page": page
            })
    
    def list_label(self):
        return self.get(f"/repos/{self.OWNER}/{self.REPO}/labels")
