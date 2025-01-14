from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB connection URI
uri = "mongodb+srv://vrdhnr:vrdhnr@my-db-1.l6cim.mongodb.net/?retryWrites=true&w=majority&appName=my-db-1"

# Step 1: Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Step 2: Ping the server to confirm connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Connection failed:", e)

# Step 3: Access a specific database and collection
db = client["my_database"]  # Replace 'my_database' with your database name
collection = db["users"]    # Replace 'users' with your collection name

# Step 4: Define a sample document (schema structure)
user = {
    "username": "johndoe",         # String: Unique username
    "age": 25,                    # Integer: User's age
    "email": "johndoe@example.com", # String: Email address
    "password": "hashed_password_123", # String: Hashed password
    "other_credentials": {        # Dictionary: Optional additional data
        "role": "admin",
        "permissions": ["read", "write"]
    }
}

# Step 5: Insert a document into the collection
insert_result = collection.insert_one(user)
print(f"User inserted with ID: {insert_result.inserted_id}")

# Step 6: Fetch all documents from the collection
print("All users in the collection:")
for document in collection.find():
    print(document)

# Step 7: Update a document (e.g., update age for a user)
update_result = collection.update_one(
    {"username": "johndoe"},       # Filter condition
    {"$set": {"age": 30}}          # Update operation
)
print(f"Matched {update_result.matched_count} document(s) and modified {update_result.modified_count} document(s).")

# Step 8: Delete a document
# delete_result = collection.delete_one({"username": "johndoe"})
# print(f"Deleted {delete_result.deleted_count} document(s).")
