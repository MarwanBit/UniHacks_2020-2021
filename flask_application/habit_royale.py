import os
from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

user1_rooms = [
    {
        "name": "Weightlifting Royale"
    },
    {
        "name": "Pure Math Research Royale"
    },
    {
        "name": "Sidhant Dubey Research Royale"
    }
]

@app.route("/")
def hello():
    return render_template('root.html', title="Habit Royale HomePage")

@app.route("/user1_homepage")
def user1_homepage():
    return render_template('user1_homepage.html', user1_rooms=user1_rooms, title = "Habit Royale Entrance")

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html',title='Register',form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html',title="Login",form=form)

if __name__ == '__main__':
    app.run(debug=True)
