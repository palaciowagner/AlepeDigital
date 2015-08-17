from app import db, app
from hashlib import md5
import re
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, current_user
from config import WHOOSH_ENABLED

import sys
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = WHOOSH_ENABLED
    if enable_search:
        import flask.ext.whooshalchemy as whooshalchemy



lm = LoginManager(app)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('deputy.id'))
)

class Votes(db.Model):
    __tablename__ = 'votes'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    project_number = db.Column(db.String(20), db.ForeignKey('project.number'), primary_key=True)
    voted_yes = db.Column(db.Boolean)
#votes = db.Table('votes',
#    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#    db.Column('project_number', db.String(20), db.ForeignKey('project.number')),
#    db.Column('voted_yes', db.Boolean)
#)

class User(UserMixin,db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('Deputy',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')
    

    @lm.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def avatar(self, size):
            return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub('[^a-zA-Z0-9_\.]', '', nickname)

    def follow(self, deputy):
        if not self.is_following(deputy):
            self.followed.append(deputy)
            return self

    def unfollow(self, deputy):
        if self.is_following(deputy):
            self.followed.remove(deputy)
            return self

    def is_following(self, deputy):
        return self.followed.filter(followers.c.followed_id == deputy.id).count() > 0

    def followed_projects(self):
        return Project.query.join(followers, (followers.c.followed_id == Project.deputy_id)).filter(followers.c.follower_id == self.id).order_by(Project.publishDate.desc())
           
    def __repr__(self):
        return '<User %r>' % (self.nickname)

    #def get_id(self):
    #    try:
    #        return unicode(self.id)  # python 2
    #    except NameError:
    #        return str(self.id)  # python 3

    

class Post(db.Model):
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Deputy(db.Model):

    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    party = db.Column(db.String(10))
    email = db.Column(db.String(50))
    job = db.Column(db.String(60))
    phone = db.Column(db.String(20))
    bio = db.Column(db.String(300))
    projects = db.relationship('Project', backref='deputy', lazy='dynamic')
    
    
    def avatar(self, size):
            return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    def __repr__(self):
        return '<Deputy %r>' % (self.name)

class Project(db.Model):

    __searchable__ = ['name','text']

    number = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50))
    text = db.Column(db.String(200))
    status = db.Column(db.String(10))
    publishDate = db.Column(db.DateTime)
    votesYes = db.Column(db.Integer, default=0)
    votesNo = db.Column(db.Integer, default=0)
    deputy_id = db.Column(db.Integer, db.ForeignKey('deputy.id'))
    voted_by = db.relationship('User',
                           secondary=Votes,
                           primaryjoin=(Votes.project_number == number),
                           backref = db.backref('voted_on', lazy = 'dynamic'),
                           lazy = 'dynamic')

    def yes(self, user):
        if self.has_voted(user):
            if not self.voted_yes(user):
                self.votesYes += 1
                self.votesNo -= 1
                                
        else:
            self.votesYes += 1 
            if not user in self.voted_by.all():
                self.voted_by.append(user)
                       
        return self

    def no(self, user):
        if self.has_voted(user):
            if self.voted_yes(user):
                self.votesNo += 1
                self.votesYes -= 1
                
        else:
            self.votesNo += 1
            if not user in self.voted_by.all():
                self.voted_by.append(user)
            
        return self
        
    def has_voted(self, user):
        return self.voted_by.filter(Votes.user_id == user.id).count() > 0

    def voted_yes(self,user):
        return self.voted_by.filter(Votes.user_id == user.id, Votes.voted_yes == True).count() > 0

    def __repr__(self):
        return '<Project %r>' % (self.number)
#enable_search = WHOOSH_ENABLED
#if enable_search:
#    import flask.ext.whooshalchemy as whooshalchemy

if enable_search:
    whooshalchemy.whoosh_index(app, Post)



