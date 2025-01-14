from pages.common.cookies_manager import initCookies
from pymongo import MongoClient
from pymongo.server_api import ServerApi
# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import Session
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

        # Step 2: Check if the variable is in MongoDB
        user_session = collection.find_one({"_id": st.session_state.user_id})
        if user_session and self.__name in user_session:
            value = user_session[self.__name]
            st.session_state[self.__name] = value
            return value

        # Step 3: Compute the variable, store it in session state and MongoDB
        value = self.__compute_func()
        st.session_state[self.__name] = value

        # Update or insert the value in MongoDB
        # datetime.datetime.fromtimestamp(time.time())
        collection.update_one(
            {"_id": st.session_state.user_id},
            {"$set": {self.__name: value, "last_updated": datetime.datetime.now()}},
            upsert=True
        )

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

if "engine" not in st.session_state:
    # MongoDB connection
    uri = "mongodb+srv://local_user:local_user@cluster0.217dt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # Create a new client and connect to the server
    st.session_state.client = MongoClient(uri, server_api=ServerApi('1'))

    # st.session_state.engine = create_engine("sqlite+pysqlite:///pages/common/databases/my_db_1.db", echo=True)

    # with Session(st.session_state.engine) as session:
    #     session.execute(
    #         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
    #         [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
    #     )
    #     session.commit()

db_name = "username"
collection_name = "workspace_name"
db = st.session_state.client[db_name]
collection = db[collection_name]
doc_count = collection.count_documents({})
print(doc_count)

var = Variable(17, 1, "")
var.value = 21
print(var.value)
