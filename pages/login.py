from hashlib import sha256
from pages.common.cookies_manager import initCookies
from pages.common.databases_manager import executeSQL
from sqlalchemy import create_engine
import streamlit as st

def checkCredentials(username: str, password: str) -> str:
    # Authentication logic
    curr_user_id = sha256(username.encode()).hexdigest()
    curr_pswd_hash = sha256(password.encode()).hexdigest()
    sql = "SELECT user_id, password_hash FROM users_credentials"
    res = executeSQL(sql, st.session_state.engine)
    return curr_user_id if any(row.user_id == curr_user_id and row.password_hash == curr_pswd_hash for row in res) else ""

cookies = initCookies()

# Ensure that the cookies are ready
if not cookies.ready():
    st.error("Cookies not initialised yet.")
    st.stop()

if cookies.get("user_id", "") != "":
    # Already logged in
    st.switch_page("./home.py")

# if "user_id" in cookies:
#     if cookies["user_id"] != "":
#         # Already logged in
#         st.switch_page("./home.py")

if "engine" not in st.session_state:
    st.session_state.engine = create_engine("sqlite+pysqlite:///pages/common/databases/server_side.db", echo=True)

st.title("Login")

username = st.text_input("Username", max_chars=256)
password = st.text_input("Password", type="password")
if st.button("Login"):
    user_id = checkCredentials(username, password)
    if user_id != "":
        st.session_state.username = username
        st.session_state.user_id = user_id
        cookies["username"] = username  # Store the username in a cookie
        cookies["user_id"] = user_id    # Store the user ID in a cookie
        cookies.save()  # Save cookies
        st.success("Logged in successfully!")
        st.rerun()
    else:
        st.error("Invalid username or password.")
