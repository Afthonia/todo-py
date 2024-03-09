from . import db


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(100))
    done = db.Column(db.Boolean)
    
    def __init__(self, task, done=False):
        self.task = task
        self.done = done