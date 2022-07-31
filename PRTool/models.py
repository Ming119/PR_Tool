from util import db

class TeamMember(db.Model):
    __tablename__ = 'TeamMember'

    id = db.Column(db.Integer, primary_key=True)

    team = db.Column(db.String(32), nullable=False)
    user = db.Column(db.String(64), nullable=False)

    @staticmethod
    def add(team, user):
        try:
            db.session.add(TeamMember(
                team=team, user=user
            ))
            db.session.commit()
            return True
        except:
            return False

    @staticmethod
    def getTeamMembers(user=None, team=None):
        if user:
            return TeamMember.query.filter_by(user=user).first()

        if team:
            return TeamMember.query.filter_by(team=team).all()

        return TeamMember.query.all()

class TeamReviewer(db.Model):
    __tablename__ = 'TeamReviewer'

    id = db.Column(db.Integer, primary_key=True)

    team     = db.Column(db.String(32), nullable=False)
    reviewer = db.Column(db.String(64), nullable=False)

    @staticmethod
    def add(team, reviewers):
        try:
            for reviewer in reviewers:
                db.session.add(TeamReviewer(
                    team=team, reviewer=reviewer
                ))
            db.session.commit()
            return True
        except:
            return False

    @staticmethod
    def clean(team):
        try:
            TeamReviewer.query.filter_by(team=team).delete()
            db.session.commit()
            return True
        except:
            return False

    @staticmethod
    def getTeamReviewers(team=None):
        if team:
            return TeamReviewer.query.filter_by(team=team).all()
        return TeamReviewer.query.all()

class TeamAssignee(db.Model):
    __tablename__ = 'TeamAssignee'

    id = db.Column(db.Integer, primary_key=True)

    team     = db.Column(db.String(32), nullable=False)
    assignee = db.Column(db.String(64), nullable=False)

    @staticmethod
    def add(team, assignees):
        try:
            for assignee in assignees:
                db.session.add(TeamAssignee(
                    team=team, assignee=assignee
                ))
            db.session.commit()
            return True
        except:
            return False

    @staticmethod
    def clean(team):
        try:
            TeamAssignee.query.filter_by(team=team).delete()
            db.session.commit()
            return True
        except:
            return False

    @staticmethod
    def getTeamAssignees(team=None):
        if team:
            return TeamAssignee.query.filter_by(team=team).all()
        return TeamAssignee.query.all()

class TeamLabel(db.Model):
    __tablename__ = 'TeamLabel'

    id = db.Column(db.Integer, primary_key=True)

    team  = db.Column(db.String(32), nullable=False)
    label = db.Column(db.String(64), nullable=False)

    @staticmethod
    def add(team, labels):
        try:
            for label in labels:
                db.session.add(TeamLabel(
                    team=team, label=label
                ))
            db.session.commit()
            return True
        except:
            return False

    @staticmethod
    def clean(team):
        try:
            TeamLabel.query.filter_by(team=team).delete()
            db.session.commit()
            return True
        except:
            return False

    @staticmethod
    def getTeamLabels(team=None):
        if team:
            return TeamLabel.query.filter_by(team=team).all()
        return TeamLabel.query.all()