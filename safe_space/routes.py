from flask import render_template, request, url_for, jsonify, flash, redirect, request, json
from safe_space import app
from safe_space.forms import RegistrationForm, LoginForm, UrlForm, DemoForm
from safe_space.models import User, Url
from safe_space.fetch_api_data import get_mod_data
from safe_space.get_url_data import url_data
from flask_bcrypt import Bcrypt
from safe_space.models import db
from flask_login import login_user, current_user, logout_user, login_required
import schedule
import time

bcrypt = Bcrypt(app)



@app.route("/", methods=['GET'])
def index():
    """ Returns application's Hompage"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    """ Handles user registration """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been successfully created!', 'success') 
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():

    """ Handles user login """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check your email and password', 'danger')
           
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    """ Displays user's dashboard """
    user_urls = current_user.urls
    url = ''    
    text = ''
    mod_report = ''
    url_endpoint = ''

    if request.method == 'POST':
        url_endpoint = request.form['url_endpoint']
        text = url_data(url_endpoint)
        # if len(text) < 10000:
        mod_report = get_mod_data(text)
        print(mod_report)            

    return render_template('dashboard.html', mod_report=mod_report,text=text, url_endpoint=url_endpoint,user_urls=user_urls)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return "User Profile"

@app.route('/text-moderation/demo', methods=['GET', 'POST'])
def demo():

    """ Handle API demo """

    form = DemoForm()
    text = ''
    mod_report = ''
    if request.method == 'POST':
        text = request.form['text']
        mod_report = get_mod_data(text)
        
    return render_template('demo.html', form=form, text=text, mod_report=mod_report)

@app.route('/url', methods=['GET', 'POST'])
def url_endpoints():

    form = UrlForm()
    if form.validate_on_submit():
        url = Url(title=form.url.data, user_id=current_user.id)
        db.session.add(url)
        db.session.commit()
        flash(f'URL saved', 'success')
        return redirect(url_for('url_endpoints'))
    
    user_urls = current_user.urls
    return render_template('urls.html', form=form, user_urls=user_urls)

