from hashlib import sha256
from streamlit_cookies_manager import EncryptedCookieManager
import streamlit as st

# Function to simulate login
def checkCredentials(username: str, password: str) -> str:
    # Authentication logic
    with open("users_credentials.txt", 'r') as fp:
        raw_lines = fp.readlines()

    for line in raw_lines:
        parts = line[:-1].split(' ')
        stored_pswd_hash = parts[-1]
        stored_usrn = ' '.join(parts[:-1])

        if username == stored_usrn and sha256(password.encode()).hexdigest() == stored_pswd_hash:
            return username # Example unique identifier

    return ""

def checkUsername(username: str) -> bool:
    with open("usernames.txt", 'r') as fp:
        raw_lines = fp.readlines()

    for line in raw_lines:
        if username == line[:-1]:
            return False

    return True

def doLoggedInStuff() -> None:
    st.header(f"Welcome {st.session_state.user_id}")

    if st.button("Logout"):
        st.session_state.pop("user_id")
        cookies["user_id"] = ""
        cookies.save()  # Save changes
        st.success("You have been logged out.")
        st.rerun()

def doLoginRegisterStuff() -> None:
    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        remember = st.checkbox("Remember me")
        if st.button("Login"):
            user_id = checkCredentials(username, password)
            if user_id != "":
                st.session_state.user_id = user_id
                if remember:
                    cookies["user_id"] = user_id    # Store the user ID in a cookie
                    cookies.save()  # Save cookies
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with register_tab:
        st.header("Register")
        with st.form("register"):
            usrn = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
            pswd = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
            c_pswd = st.text_input("Confirm password", type="password", placeholder="Confirm password", label_visibility="collapsed")
            submitted = st.form_submit_button("Register")
            if submitted:
                if usrn != "":
                    if checkUsername(usrn):
                        if pswd == c_pswd:
                            pswd_hash = sha256(pswd.encode()).hexdigest()
                            with open("usernames.txt", 'a') as fp:
                                fp.write(f"{usrn}\n")
                            with open("users_credentials.txt", 'a') as fp:
                                fp.write(f"{usrn} {pswd_hash}\n")
                            st.success("Registered successfully!")
                            st.rerun()
                        else:
                            st.error("Passwords don't match.")
                    else:
                        st.error("Username is taken.")
                else:
                    st.error("Enter a username.")

# Create a cookie manager (use a strong secret key)
cookies = EncryptedCookieManager(prefix="my_app", password="your_secure_password")

# Must be run to load existing cookies
if not cookies.ready():
    st.stop()

# Check for existing login
if "user_id" in cookies:
    if cookies["user_id"] != "":
        st.session_state.user_id = cookies["user_id"]

if "user_id" in st.session_state:
    doLoggedInStuff()
else:
    doLoginRegisterStuff()
