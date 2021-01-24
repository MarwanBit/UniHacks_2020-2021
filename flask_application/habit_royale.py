import os

from flask import Flask, render_template
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
    return render_template('root.html')

@app.route("/user1_homepage")
def user1_homepage():
    return render_template('user1_homepage.html', user1_rooms=user1_rooms)

if __name__ == '__main__':
    app.run(debug=True)
