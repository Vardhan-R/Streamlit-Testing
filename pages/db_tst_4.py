from datetime import datetime
from pymongo import MongoClient
import streamlit as st

class Variable:
    def __init__(self, value) -> None:
        self._value = value
        self._type = type(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value) -> None:
        self._value = new_value
        self._type = type(new_value)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_type) -> None:
        raise AttributeError("Cannot modify `type` directly, as it is derived from `value`.")

a = Variable(8)
print(a.value)
b = a
print(b)
print(b.type)

exit()

# MongoDB connection
uri = "mongodb+srv://vrdhnr:vrdhnr@my-db-1.l6cim.mongodb.net/?retryWrites=true&w=majority&appName=my-db-1"
client = MongoClient(uri)
db = client["my_database"]
session_collection = db["users"]

def get_or_compute_variable(user_id: str, var_name: str, compute_fn):
    """
    Retrieves a variable from st.session_state or MongoDB.
    If not found, computes it using the provided function and stores it.

    Parameters:
    - user_id: Unique identifier for the user/session.
    - var_name: The name of the variable to retrieve.
    - compute_fn: A function to compute the variable if it doesn't exist.

    Returns:
    - The value of the variable.
    """
    # Step 1: Check if the variable is in session state
    if var_name in st.session_state:
        return st.session_state[var_name]

    # Step 2: Check if the variable is in MongoDB
    user_session = session_collection.find_one({"_id": user_id})
    if user_session and var_name in user_session:
        value = user_session[var_name]
        st.session_state[var_name] = value
        return value

    # Step 3: Compute the variable, store it in session state and MongoDB
    value = compute_fn()
    st.session_state[var_name] = value

    # Update or insert the value in MongoDB
    session_collection.update_one(
        {"_id": user_id},
        {"$set": {var_name: value, "last_updated": datetime.now()}},
        upsert=True
    )

    return value

# Example usage
def compute_x():
    # Replace with the actual computation logic for "x"
    return "computed_value_of_x"

# Unique user/session identifier (e.g., from cookies, login, etc.)
user_id = "user123"

# Get or compute the variable
x = get_or_compute_variable(user_id, "x", compute_x)

# Display the variable
st.write(f"Value of x: {x}")
