from pages.common.cookies_manager import initCookies
from pages.common.databases_manager import executeSQL
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import datetime
import streamlit as st

class Variable:
    def __init__(self, value, compute_function, name: str, index: int | None = None):
        self.value = value
        self.__type = type(value)
        self.__compute_func = compute_function
        self.__name = name
        self.__index = index

    @property
    def value(self):
        ...

    @property
    def weak_value(self):
        ...

    @property
    def strong_value(self):
        ...

    @value.getter
    def value(self):
        """
        Retrieves a variable from `st.session_state` or MongoDB.
        If not found, computes it using the provided function and stores it.

        Returns:
        - The value of the variable.
        """

        print("Getter called")

        # Step 1: Check if the variable is in session state
        if self.__name in st.session_state:
            return st.session_state[self.__name]

        # Step 2: Check if the variable is in the user's database
        sql = "SELECT ... FROM ... WHERE ..."
        params = None
        res = executeSQL(sql, st.session_state.engine, params=params)
        # user_session = collection.find_one({"_id": st.session_state.user_id})
        # if user_session and self.__name in user_session:
        #     value = user_session[self.__name]
        #     st.session_state[self.__name] = value
        #     return value

        # Step 3: Compute the variable, store it in session state and MongoDB
        value = self.__compute_func()
        st.session_state[self.__name] = value

        # Update or insert the value in the user's database
        # datetime.datetime.fromtimestamp(time.time())
        # collection.update_one(
        #     {"_id": st.session_state.user_id},
        #     {"$set": {self.__name: value, "last_updated": datetime.datetime.now()}},
        #     upsert=True
        # )

        return value

    @weak_value.getter
    def weak_value(self):
        return self.value

    @strong_value.getter
    def strong_value(self):
        return self.value

    @value.setter
    def value(self, new_value):
        self.weak_value = new_value

    @weak_value.setter
    def weak_value(self, new_value):
        print("Weak setter called")

        # Update session state
        st.session_state[self.__name] = new_value

    @strong_value.setter
    def strong_value(self, new_value):
        print("Strong setter called")

        # Step 1: Update session state
        st.session_state[self.__name] = new_value

        # Step 2: Update database

    # def __setattr__(self, name, value):
    #     match name:
    #         case "__value":
    #             raise AttributeError(f"Can't set `{name}`")

cookies = initCookies()

# Ensure that the cookies are ready
if not cookies.ready():
    st.error("Cookies not initialised yet.")
    st.stop()

if cookies.get("user_id", "") != "" and "engine" not in st.session_state:
    # Logged in
    st.session_state.engine = create_engine(f"sqlite+pysqlite:///pages/common/databases/users/db_{cookies["user_id"]}.db", echo=True)
    sql = """
    CREATE TABLE IF NOT EXISTS ... (
        ...,
        ...,
        ...
    )
    """
    executeSQL(sql, st.session_state.engine, True)
else:
    st.switch_page("./home.py")
