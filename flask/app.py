from flask import Flask, redirect, render_template, request, url_for
from flask_restful import Api, Resource
# from flask_pymongo import PyMongo
# from pymongo import MongoClient
from flask_sqlalchemy import SQLAlchemy

uri = "mongodb+srv://interastral_guide01:Z2sFxJB4uhSe1btC@interastralguidetest01.0yhgl.mongodb.net/interastral_guide01?retryWrites=true&w=majority"

app = Flask(__name__)

# app.config["MONGO_URI"] = uri
# db = mongo._database = PyMongo(app).db

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# mongo = PyMongo(app)

# client = MongoClient(uri)
# try:
#     # Attempt to ping the database
#     client.admin.command('ping')
#     print("MongoDB connection successful!")
# except Exception as e:
#     print("MongoDB connection failed:", e)
# finally:
#     # Close the connection
#     client.close()

# class Character(Resource):
#     def get(self):
#         characters = mongo.db.characters.find()
#         return [{"id": str(character["_id"]), "name": character["name"], "power": character["power"]} for character in characters]

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# Make sure this is wrapped inside an application context
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    # todo_list = Todo.query.all()
    todo_list = db.session.query(Todo).all()
    # return "Hello, World!"
    return render_template("base.html", todo_list=todo_list)


# @app.route("/add", methods=["POST"])
@app.post("/add")
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.get("/update/<int:todo_id>")
def update(todo_id):
    # todo = Todo.query.filter_by(id=todo_id).first()
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.get("/delete/<int:todo_id>")
def delete(todo_id):
    # todo = Todo.query.filter_by(id=todo_id).first()
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

# @app.route('/insert_sample_data')
# def insert_sample_data():
#     sample_data = [
#         {"name": "Character One", "power": "Fire"},
#         {"name": "Character Two", "power": "Water"},
#     ]
#     try:
#         db.characters.insert_many(sample_data)
#         return "Sample data inserted!", 201  # Returning a 201 Created status
#     except Exception as e:
#         return str(e), 500  # Return error message with a 500 Internal Server Error status


# api = Api(app)
# api.add_resource(Character, '/api/characters')

# if __name__ == '__main__':
#     app.run(debug=True)
