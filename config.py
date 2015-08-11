# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

#Searching
WHOOSH_BASE = os.path.join(basedir, 'search.db')

# Whoosh does not work on Heroku
WHOOSH_ENABLED = os.environ.get('HEROKU') is None

MAX_SEARCH_RESULTS = 50

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = 'palaciowagner'
MAIL_PASSWORD = '12345'

# pagination
POSTS_PER_PAGE = 3

# administrator list
ADMINS = ['palaciowagner@yahoo.com.br']

#OPENID_PROVIDERS = [
#    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
#    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
#    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
#    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
#    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]
	

OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '1603622893225211',
        'secret': '7a3989113f51e25916e51e2936692167'
    }
}

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

LANGUAGES = {
    'en': 'English',
    'pt': 'Português',
    'en':'español'
}

