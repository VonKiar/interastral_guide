from pymongo import MongoClient

# Replace the connection string with your actual MongoDB connection string
uri = "mongodb+srv://interastral_guide01:Z2sFxJB4uhSe1btC@interastralguidetest01.0yhgl.mongodb.net/db1?retryWrites=true&w=majority"

# Initialize MongoClient
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
