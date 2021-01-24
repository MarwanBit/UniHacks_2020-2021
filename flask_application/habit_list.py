import os

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello World :)!</h1>"

@app.route("/user1_homepage")
def user1_homepage():
    return "<h1>Welcome user1 :)</h1>"

if __name__ == '__main__':
    app.run(debug=True)
