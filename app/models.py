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
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)



class User(UserMixin,db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    @lm.user_loader
    def load_user(id):
        return User.query.get(int(id))

    #@app.route('/authorize/<provider>')
    #def oauth_authorize(provider):
    #    if not current_user.is_anonymous():
    #        return redirect(url_for('index'))
    #    oauth = OAuthSignIn.get_provider(provider)
    #    return oauth.authorize()

    #@app.route('/callback/<provider>')
    #def oauth_callback(provider):
    #    if not current_user.is_anonymous():
    #        return redirect(url_for('index'))
    #    oauth = OAuthSignIn.get_provider(provider)
    #    social_id, username, email = oauth.callback()
    #    if social_id is None:
    #        flash('Authentication failed.')
    #        return redirect(url_for('index'))
    #    user = User.query.filter_by(social_id=social_id).first()
    #    if not user:
    #        user = User(social_id=social_id, nickname=username, email=email)
    #        db.session.add(user)
    #        db.session.commit()
    #    login_user(user, True)
    #    return redirect(url_for('index'))


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

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

   
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

class Deputado(db.Model):

    __searchable__ = ['nome']

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    partido = db.Column(db.String(10))
    email = db.Column(db.String(50))
    profissao = db.Column(db.String(60))
    telefone = db.Column(db.String(20))
    biografia = db.Column(db.String(300))
    projetos = db.relationship('Projeto', backref='deputado', lazy='dynamic')

    def avatar(self, size):
            return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    def __repr__(self):
        return '<Deputado %r>' % (self.nome)

class Projeto(db.Model):

    __searchable__ = ['nome','texto']

    numero = db.Column(db.String(20), primary_key=True)
    nome = db.Column(db.String(50))
    texto = db.Column(db.String(200))
    status = db.Column(db.String(10))
    dataPublicacao = db.Column(db.DateTime)
    deputado_id = db.Column(db.Integer, db.ForeignKey('deputado.id'))

    def __repr__(self):
        return '<Projeto %r>' % (self.numero)
#enable_search = WHOOSH_ENABLED
#if enable_search:
#    import flask.ext.whooshalchemy as whooshalchemy

if enable_search:
    whooshalchemy.whoosh_index(app, Post)



