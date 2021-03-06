﻿from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, babel
from .forms import LoginForm, EditForm, PostForm, SearchForm
from .models import User, Post, Deputy, Project, Votes
from datetime import datetime
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS,LANGUAGES
from flask.ext.babel import gettext
from OAuth import OAuthSignIn

@babel.localeselector
def get_locale():
	#return request.accept_languages.best_match(LANGUAGES.keys())
	return 'pt'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
#@login_required
def index(page=1):
    form = PostForm()
    if form.validate_on_submit():
		post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=g.user)
		db.session.add(post)
		db.session.commit()
		flash(gettext('Your post is now live!'))
		return redirect(url_for('index'))   
    
    if g.user is not None and g.user.is_authenticated():
        projects = g.user.followed_projects().paginate(page, POSTS_PER_PAGE, False)
        return render_template('index.html',
						       title='Home',
						       form=form,
						       projects=projects)
    else:
        return redirect(url_for('login'))

						   
##Load User function						   
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))

##Login Function						   
@app.route('/login', methods=['GET', 'POST'])
#@oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	#form = LoginForm()
	#if form.validate_on_submit():
	#	session['remember_me'] = form.remember_me.data
	#	return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
	return render_template('login.html',
						   title='Sign In')

###After Login
#@oid.after_login
#def after_login(resp):


#	if resp.email is None or resp.email == "":
#		flash(gettext('Invalid login. Please try again.'))
#		return redirect(url_for('login'))
#	user = User.query.filter_by(email=resp.email).first()
#	if user is None:
#		nickname = resp.nickname
#		if nickname is None or nickname == "":
#			nickname = resp.email.split('@')[0]
#		nickname = User.make_valid_nickname(nickname)
#		nickname = User.make_unique_nickname(nickname)
#		user = User(nickname = nickname, email = resp.email)
#		db.session.add(user)
#		db.session.commit()
#		db.session.add(user.follow(user))
#		db.session.commit()
#	remember_me = False
#	if 'remember_me' in session:
#		remember_me = session['remember_me']
#		session.pop('remember_me', None)
#	login_user(user, remember = remember_me)


#	return redirect(request.args.get('next') or url_for('index'))
		
##Before Request		
@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated():
		g.user.last_seen = datetime.utcnow()
        #db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()
	g.locale = get_locale()
	
##Logout Function
#@app.route('/logout')
#def logout():
#	logout_user()
#	return redirect(url_for('index'))
	
##View de user
@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
	user = User.query.filter_by(nickname=nickname).first()
	if user == None:
		flash(gettext('User %(usr)s not found.', usr=nickname))
		return redirect(url_for('index'))
	posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
	return render_template('user.html',
						   user=user,
						   posts=posts)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
	form = EditForm(g.user.nickname)
	if form.validate_on_submit():
		g.user.nickname = form.nickname.data
		g.user.about_me = form.about_me.data
		db.session.add(g.user)
		db.session.commit()
		flash(gettext('Your changes have been saved.'))
		return redirect(url_for('edit'))
	else:
		form.nickname.data = g.user.nickname
		form.about_me.data = g.user.about_me
	return render_template('edit.html', form=form)

@app.route('/follow/<name>')
@login_required
def follow(name):
	#user = User.query.filter_by(nickname=nickname).first()
    deputy = Deputy.query.filter_by(name=name).first()
    if deputy is None:
		flash(gettext('Deputy %(dep)s not found.', dep= name))
		return redirect(url_for('index'))
   
    u = g.user.follow(deputy)
    if u is None:
		flash(gettext('Cannot follow %(dep)s.', dep=name ))
		return redirect(url_for('deputy', name=name))
    db.session.add(u)
    db.session.commit()
    flash(gettext('You are now following %(dep)s', dep = name))
    return redirect(url_for('deputy', name=name))

@app.route('/unfollow/<name>')
@login_required
def unfollow(name):
	deputy = Deputy.query.filter_by(name=name).first()
	if deputy is None:
		flash(gettext('Deputy %(dep)s not found.', dep= name))
		return redirect(url_for('index'))
	
	u = g.user.unfollow(deputy)
	if u is None:
		flash(gettext('Cannot unfollow %(dep)s.', dep=name ))
		return redirect(url_for('deputy', name=name))
	db.session.add(u)
	db.session.commit()
	flash(gettext('You have stopped following %(dep)s',dep = name ))
	return redirect(url_for('deputy',name=name))

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get(id)
    if post is None:
        flash('Post not found.')
        return redirect(url_for('index'))
    if post.author.id != g.user.id:
        flash('You cannot delete this post.')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.')
    return redirect(url_for('index'))



@app.route('/votar/sim/<projectNumber>')
@login_required
def yes(projectNumber):
    project = Project.query.filter_by(number=projectNumber).first()

    if project is None:
        flash(gettext('Project %(number)s not found.', number = projectNumber))
        return redirect(url_for('index'))
    p = project.yes(g.user)
    v = Votes(user_id=g.user.id, project_number=projectNumber, voted_yes=True)
    if p is None:
        flash(gettext('Cannot vote for %(project)s project', project=projectNumber ))
        return redirect(url_for('index'))
    db.session.add(p)
    db.session.add(v)
    db.session.commit()
    flash(gettext('Thanks for voting for %(project)s', project=projectNumber ))
    return redirect(url_for('index'))

@app.route('/votar/nao/<projectNumber>')
@login_required
def no(projectNumber):
    project = Project.query.filter_by(number=projectNumber).first()
    if project is None:
        flash(gettext('Project %(number)s not found.', number = projectNumber))
        return redirect(url_for('index'))
    p = project.no(g.user)
    v = Votes(user_id=g.user.id, project_number=projectNumber, voted_yes=True)
    if p is None:
        flash(gettext('Cannot vote for %(project)s project', project=projectNumber ))
        return redirect(url_for('index'))
    db.session.add(p)
    db.session.add(v)
    db.session.commit()
    flash(gettext('Thanks for voting for %(project)s', project=projectNumber ))
    return redirect(url_for('index'))

#####ERROR HANDLERS######
@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500

@app.route('/search', methods=['POST'])
@login_required
def search():
	if not g.search_form.validate_on_submit():
		return redirect(url_for('index'))
	return redirect(url_for('search_results', query=g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
	results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
	return render_template('search_results.html',
						   query=query,
						   results=results)


@app.route('/deputados/<query>')
def deputados(query):
    if query == 'all':
        results = Deputy.query.all()
        return render_template('deputados.html',
						   query=query,
						   results=results)

##View de Deputy
@app.route('/deputado/<name>')
@app.route('/deputado/<name>/<int:page>')
@login_required
def deputy(name, page=1):
    
	deputy = Deputy.query.filter_by(name=name).first()
	if deputy == None:
		flash(gettext('Deputy %(usr)s not found.', usr=name))
		return redirect(url_for('index'))
	projects = deputy.projects.paginate(page, POSTS_PER_PAGE, False)
	return render_template('deputy.html',
						   deputy=deputy,
						   projects=projects)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)