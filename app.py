from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
#from json_responses import json_req

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo-list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.register_blueprint(json_req)

from models.todo_model import db, Todo



@app.route("/")
def index():
    return render_template("index.html", todos=Todo.query.all())

@app.route("/add", methods=["POST"])
def add():
    todo = request.form["task"]
    if todo != "":
        task = Todo(todo, False)
        db.session.add(task)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    #id = request.args.get('id')
    todo = Todo.query.filter_by(id=id).first()
    if request.method == "POST":
        todo.task = request.form["task"]
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todo=todo, id=id)


@app.route("/check/<int:id>")
def check(id):
    found_todo = Todo.query.filter_by(id=id).first()
    found_todo.done = not found_todo.done
    db.session.commit()
    
    return redirect(url_for("index"))

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
    found_todo = Todo.query.filter_by(id=id).first()
    db.session.delete(found_todo)
    db.session.commit()
    
    return redirect(url_for("index"))


@app.route("/todo/list")
def getAll():
    todos = Todo.query.all()
    data = []

    for task in todos:
        data.append({
            "id": task.id,
            "task": task.task,
            "done": task.done,
        })

    return jsonify({
        "tasks": data
    })

@app.route("/todo/add", methods=["POST"])
def addTask():
    data = request.get_json()
    todo = data['task']
    if todo != "":
        task = Todo(todo, False)
        db.session.add(task)
        db.session.commit()
    return jsonify({
        "id": task.id,
        "task": task.task,
        "done": task.done
    })

@app.route("/todo/edit/<int:id>", methods=["GET", "POST"])
def editTask(id):
    #id = request.args.get('id')
    todo = Todo.query.filter_by(id=id).first()
    if request.method == "POST":
        todo.task = request.get_json()["task"]
        db.session.commit()
        return jsonify({
            "id": todo.id,
            "task": todo.task,
            "done": todo.done
        })
    else:
        return jsonify({
            "error": "invalid request"
        })


@app.route("/todo/check/<int:id>")
def checkTask(id):
    found_todo = Todo.query.filter_by(id=id).first()
    found_todo.done = not found_todo.done
    db.session.commit()
    
    return jsonify({
        "id": found_todo.id,
        "task": found_todo.task,
        "done": found_todo.done
    })

@app.route("/todo/delete/<int:id>", methods=["DELETE"])
def deleteTask(id):
    found_todo = Todo.query.filter_by(id=id).first()
    db.session.delete(found_todo)
    db.session.commit()
    
    return jsonify({
        "success": "deleted successfully"
    })

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8081, debug=True)