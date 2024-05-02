from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy

json_req = Blueprint('json_req', __name__)

from models.todo_model import db, Todo


@json_req.route("/todo/list")
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

@json_req.route("/todo/add", methods=["POST"])
def addTask():
    data = request.get_json()
    todo = data['task']
    if todo != "":
        task = Todo(todo, False)
        db.session.add(task)
        db.session.commit()
    return jsonify({
        "id": todo.id,
            "task": todo.task,
            "done": todo.done
    })

@json_req.route("/todo/edit/<int:id>", methods=["GET", "POST"])
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


@json_req.route("/todo/check/<int:id>")
def checkTask(id):
    found_todo = Todo.query.filter_by(id=id).first()
    found_todo.done = not found_todo.done
    db.session.commit()
    
    return jsonify({
        "id": found_todo.id,
        "task": found_todo.task,
        "done": found_todo.done
    })

@json_req.route("/todo/delete/<int:id>", methods=["DELETE"])
def deleteTask(id):
    found_todo = Todo.query.filter_by(id=id).first()
    db.session.delete(found_todo)
    db.session.commit()
    
    return jsonify({
        "success": "deleted successfully"
    })