from hashlib import sha256
from pages.common.cookies_manager import initCookies
from pages.common.databases_manager import executeSQL
from sqlalchemy import create_engine
import streamlit as st

def checkUsername(username: str) -> bool:
    curr_user_id = sha256(username.encode()).hexdigest()
    sql = "SELECT user_id FROM users_credentials"
    res = executeSQL(sql, st.session_state.engine)
    return all(row.user_id != curr_user_id for row in res)

cookies = initCookies()

# Ensure that the cookies are ready
if not cookies.ready():
    st.error("Cookies not initialised yet.")
    st.stop()

if cookies.get("user_id", "") != "":
    # Already logged in
    st.switch_page("./home.py")

if "engine" not in st.session_state:
    st.session_state.engine = create_engine("sqlite+pysqlite:///pages/common/databases/server_side.db", echo=True)

st.title("Register")

with st.form("register"):
    usrn = st.text_input("Username", max_chars=256, placeholder="Username", label_visibility="collapsed")
    pswd = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
    c_pswd = st.text_input("Confirm password", type="password", placeholder="Confirm password", label_visibility="collapsed")
    submitted = st.form_submit_button("Register")
    if submitted:
        if usrn != "":
            if checkUsername(usrn):
                if pswd == c_pswd:
                    sql = "INSERT INTO users_credentials (username, password_hash, user_id) VALUES (:usrn, :pswd_hash, :usr_id)"
                    params = [{"usrn": usrn, "pswd_hash": sha256(pswd.encode()).hexdigest(), "usr_id": sha256(usrn.encode()).hexdigest()}]
                    executeSQL(sql, st.session_state.engine, True, params)
                    st.success("Registered successfully!")
                    st.switch_page("./pages/login.py")
                else:
                    st.error("Passwords don't match.")
            else:
                st.error("Username is taken.")
        else:
            st.error("Enter a username.")
