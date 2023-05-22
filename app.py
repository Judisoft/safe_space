from flask import Flask, render_template

app = Flask(__name__)

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


@app.route('/dashboard', methods=['GET'])
def dashboard():

    """ Displays user's dashboard """

    return render_template('dashboard.html')

if __name__ == "__main__":

    app.run(debug=True)