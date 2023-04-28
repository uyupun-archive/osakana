from pymongo import MongoClient

username = "root"
password = "password"
uri = f"mongodb://{username}:{password}@localhost:27017/"
client = MongoClient(uri)

db = client["my_db"]
collection = db["my_collection"]
document = {
    "name": "John Doe",
    "age": 30,
    "city": "New York"
}

result = collection.insert_one(document)
print("Inserted document with ID:", result.inserted_id)
