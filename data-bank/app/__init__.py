from flask import Flask
from flask_restful import Api, Resource
from flask_pymongo import PyMongo
from pymongo import MongoClient

uri = "mongodb+srv://interastral_guide01:Z2sFxJB4uhSe1btC@interastralguidetest01.0yhgl.mongodb.net/interastral_guide01?retryWrites=true&w=majority"

app = Flask(__name__)
app.config["MONGO_URI"] = uri

mongo = PyMongo(app)

client = MongoClient(uri)
try:
    # Attempt to ping the database
    client.admin.command('ping')
    print("MongoDB connection successful!")
except Exception as e:
    print("MongoDB connection failed:", e)
finally:
    # Close the connection
    client.close()

db = mongo._database = PyMongo(app).db

class Character(Resource):
    def get(self):
        characters = mongo.db.characters.find()
        return [{"id": str(character["_id"]), "name": character["name"], "power": character["power"]} for character in characters]

def home():
    return "Welcome to the Interastral Guide API!"

@app.route('/insert_sample_data')
def insert_sample_data():
    sample_data = [
        {"name": "Character One", "power": "Fire"},
        {"name": "Character Two", "power": "Water"},
    ]
    try:
        db.characters.insert_many(sample_data)
        return "Sample data inserted!", 201  # Returning a 201 Created status
    except Exception as e:
        return str(e), 500  # Return error message with a 500 Internal Server Error status


api = Api(app)
api.add_resource(Character, '/api/characters')

if __name__ == '__main__':
    app.run(debug=True)
