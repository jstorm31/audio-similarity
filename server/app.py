import datetime
import os
from dotenv import load_dotenv

from flask import Flask, Response, request
from flask_mongoengine import MongoEngine

load_dotenv()

app = Flask(__name__)

host = os.getenv('MONGODB_HOST')
username = os.getenv('MONGO_INITDB_ROOT_USERNAME')
password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
database = os.getenv('MONGO_INITDB_DATABASE')

app.config['MONGODB_SETTINGS'] = {
    'connect': False,
    'host': 'mongodb://' + username + ':' + password + '@' + host + ':27017' + '/' + database + '?authSource=admin'
}

db = MongoEngine()
db.init_app(app)


class Todo(db.Document):
    title = db.StringField(max_length=60)
    text = db.StringField()
    done = db.BooleanField(default=False)
    pub_date = db.DateTimeField(default=datetime.datetime.now)


@app.route("/api")
def index():
    Todo.objects().delete()
    Todo(title="Simple todo A", text="12345678910").save()
    Todo(title="Simple todo B", text="12345678910").save()
    Todo.objects(title__contains="B").update(set__text="Hello world")
    todos = Todo.objects().to_json()
    return Response(todos, mimetype="application/json", status=200)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
