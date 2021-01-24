from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(hours=24)

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/")
def home():
    if "user" in session:
        user = session["user"]
        flash(f"Welcome back, {user}!")
        return redirect(url_for("user"))
    return render_template("homepage.html")


@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        if user:
            found_user = users.query.filter_by(name=user).first()
            if found_user:
                flash("Login Successful!")
                session["user"] = user
                return redirect(url_for("user"))
            else:
                flash("User does not exist!")
                return redirect(url_for("login"))

        else:
            flash("Enter a name!")
            return redirect(url_for("login"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))

        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    goal = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            goal = request.form["email"]
            session["email"] = goal
            found_user = users.query.filter_by(name=user).first()
            found_user.email = goal
            db.session.commit()
            flash("Habit was saved!")
        else:
            if "email" in session:
                goal = session["email"]

        return render_template("user.html", user=user)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        if user:
            found_user = users.query.filter_by(name=user).first()
            if found_user:
                flash("User already exists!")
                return redirect(url_for("signup"))
            else:
                usr = users(user, "")
                db.session.add(usr)
                db.session.commit()
                session["user"] = user
                flash("User created!")
                return redirect(url_for("user"))
        else:
            flash("Enter a name!")
            return redirect(url_for("signup"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))

        return render_template("signup.html")


@app.route('/ingame', methods=['POST', 'GET'])
def ingame():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for("ingame"))
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('ingame.html', tasks=tasks, email=session["email"])


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for("ingame"))
    except:
        return 'There was an issue deleting your task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect(url_for("ingame"))
        except:
            return 'There was an error updating'
    else:
        return render_template('update.html', task=task)


@app.route("/logout")
def logout():
    user = session["user"]
    flash(f"You have been logged out, {user}!", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run(host='localhost', debug=True)
