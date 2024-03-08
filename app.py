from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo-list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app=app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(100))
    done = db.Column(db.Boolean)
    
    def __init__(self, task, done=False):
        self.task = task
        self.done = done

@app.route("/")
def index():
    return render_template("index.html", todos=Task.query.all())

@app.route("/add", methods=["POST"])
def add():
    todo = request.form["todo"]
    if todo != "":
        task = Task(todo, False)
        db.session.add(task)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    todo = Task.query.filter_by(id=id).first()
    if request.method == "POST":
        todo.task = request.form["task"]
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todo=todo, id=id)


@app.route("/check/<int:id>")
def check(id):
    found_todo = Task.query.filter_by(id=id).first()
    found_todo.done = not found_todo.done
    db.session.commit()
    
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    found_todo = Task.query.filter_by(id=id).first()
    db.session.delete(found_todo)
    db.session.commit()
    
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)