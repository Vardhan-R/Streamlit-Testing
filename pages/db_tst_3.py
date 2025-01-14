from hashlib import sha256
import streamlit as st
from pymongo import MongoClient

# MongoDB connection
uri = "mongodb+srv://vrdhnr:vrdhnr@my-db-1.l6cim.mongodb.net/?retryWrites=true&w=majority&appName=my-db-1"
client = MongoClient(uri)
db = client["my_database"]
users_collection = db["users"]

# Function to check login credentials
def check_credentials(username: str, password: str) -> str:
    user = users_collection.find_one({"username": username})
    if user and user["password"] == sha256(password.encode()).hexdigest():
        return username
    return ""

# Function to check if username is available
def is_username_available(username: str) -> bool:
    return users_collection.find_one({"username": username}) is None

# Function to handle logged-in state
def do_logged_in_stuff() -> None:
    st.header(f"Welcome {st.session_state.user_id}")
    if st.button("Logout"):
        st.session_state.pop("user_id")
        st.success("You have been logged out.")
        st.rerun()

# Function to handle login and registration
def do_login_register_stuff() -> None:
    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user_id = check_credentials(username, password)
            if user_id != "":
                st.session_state.user_id = user_id
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with register_tab:
        st.header("Register")
        with st.form("register"):
            username = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
            password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
            confirm_password = st.text_input("Confirm password", type="password", placeholder="Confirm password", label_visibility="collapsed")
            submitted = st.form_submit_button("Register")
            if submitted:
                if username != "":
                    if is_username_available(username):
                        if password == confirm_password:
                            password_hash = sha256(password.encode()).hexdigest()
                            users_collection.insert_one({"username": username, "password": password_hash})
                            st.success("Registered successfully!")
                            st.rerun()
                        else:
                            st.error("Passwords don't match.")
                    else:
                        st.error("Username is taken.")
                else:
                    st.error("Enter a username.")

# Main logic
if "user_id" in st.session_state:
    do_logged_in_stuff()
else:
    do_login_register_stuff()
