from flask import Flask, render_template, request, url_for, jsonify
from get_url_data import url_data
from fetch_api_data import get_mod_data

app = Flask(__name__)

@app.route("/url", methods=['GET', 'POST'])
def get_url():
    """ Gets the url to moderated and returns the moderation report """
    url = ''
    data = ''

    if request.method == 'POST':
        url = request.form['url']
        data = url_data(url)

    return render_template('test_form.html', url=url, data=data)

@app.route("/", methods=['GET'])
def index():
    """ Returns application's Hompage"""
    return render_template('index.html')

@app.route('/register', methods=['GET'])
def register():

    """ Handles application registration """

    return render_template('register.html')

@app.route('/login', methods=['GET'])
def login():

    """ Handles application login """

    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    """ Displays user's dashboard """
    text = 'Contact rick(at)gmail(dot)com to have s_*_x'

    mod_report = get_mod_data(text)

    return render_template('dashboard.html', mod_report=mod_report)

if __name__ == "__main__":

    app.run(debug=True)