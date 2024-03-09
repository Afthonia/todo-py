from flask_sqlalchemy import SQLAlchemy
from __main__ import app


db = SQLAlchemy(app=app)