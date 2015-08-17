# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = 'palaciowagner'
MAIL_PASSWORD = '12345'

# pagination
POSTS_PER_PAGE = 3
MAX_SEARCH_RESULTS = 50

# administrator list
ADMINS = ['palaciowagner@yahoo.com.br']

#OPENID_PROVIDERS = [
#    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
#    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
#    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
#    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
#    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]
	

if os.environ.get('HEROKU') is not None:
    id = '1603622893225211'
    secret = '7a3989113f51e25916e51e2936692167'
else:
    id = '1608245126096321'
    secret = '320e1f2a64de3e9bdeee980e1e6a281c'

OAUTH_CREDENTIALS = {
    'facebook': {

        'id': id,
        'secret': secret
    }
}

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True
WHOOSH_BASE = os.path.join(basedir, 'search.db')

# Whoosh does not work on Heroku
WHOOSH_ENABLED = os.environ.get('HEROKU') is None

LANGUAGES = {
    'en': 'English',
    'pt': 'Português',
    'en':'español'
}

