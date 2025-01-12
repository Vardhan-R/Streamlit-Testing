import pymysql
import streamlit as st

def interact() -> None:
    my_db = pymysql.connect(host="localhost", user="root", password="root")
    my_cursor = my_db.cursor()

    sql = """
    CREATE DATABASE test_db;
    """
    my_cursor.execute(sql)
    my_db.commit()

    my_cursor.execute("USE test_db;")
    my_db.commit()

    sql = """
    CREATE TABLE all_users (
        username VARCHAR(255) NOT NULL,
        age INT,
        PRIMARY KEY (username)
    );
    """
    my_cursor.execute(sql)
    my_db.commit()

    sql = "INSERT IGNORE INTO all_users VALUES (%s, %s);"
    my_cursor.executemany(sql, (("Vardhan", 20), ("Second person", 21)))
    my_db.commit()

    res = my_cursor.execute("SELECT * FROM all_users;")

    sql = """
    DROP TABLE all_users;
    """
    my_cursor.execute(sql)
    my_db.commit()

    my_cursor.execute("DROP DATABASE test_db;")
    my_db.commit()

    my_cursor.close()
    my_db.close()

    return res

def executeSQL(cursor, sql, database=None, values=None, fetch=False):
    res = cursor.executemany(sql, values) if values else cursor.execute(sql)

    if database:
        database.commit()

    if fetch:
        return cursor.fetchall()

st.set_page_config("DBMS")
st.title("DBMS")

all_sql = [
    "CREATE DATABASE test_db;",
    "USE test_db;",
    """
    CREATE TABLE all_users (
        username VARCHAR(255) NOT NULL,
        age INT,
        PRIMARY KEY (username)
    );
    """,
    "INSERT IGNORE INTO all_users VALUES (%s, %s);",
    "SELECT * FROM all_users;",
    "DROP TABLE all_users;",
    "DROP DATABASE test_db;"
]

all_vals = [
    None,
    None,
    None,
    (("Vardhan", 20), ("Second person", 21)),
    None,
    None,
    None
]

all_fetches = [
    False,
    False,
    False,
    False,
    True,
    False,
    False
]

if st.button("Connect"):
    if "my_cursor" not in st.session_state:
        st.session_state.my_db = pymysql.connect(host="192.168.209.81", user="root", password="root")
        st.session_state.my_cursor = st.session_state.my_db.cursor()
        st.success("Successfully connected!")

for i, (sql, vals, fetch) in enumerate(zip(all_sql, all_vals, all_fetches), 1):
    if st.button(sql, i):
        res = executeSQL(st.session_state.my_cursor, sql, st.session_state.my_db, vals, fetch)
        if sql.split(' ')[0] == "SELECT":
            for row in res:
                st.write(row)
        st.success(f"Successfully executed {sql}!")

if st.button("Disconnect"):
    st.session_state.my_cursor.close()
    st.session_state.my_db.close()
    st.success("Successfully disconnected!")

if st.button("Execute SQL"):

    c_db = "CREATE DATABASE test_db;"
    u_db = "USE test_db;"
    c_tb = """
    CREATE TABLE all_users (
        username VARCHAR(255) NOT NULL,
        age INT,
        PRIMARY KEY (username)
    );
    """
    ins = "INSERT IGNORE INTO all_users VALUES (%s, %s);"
    vals = (("Vardhan", 20), ("Second person", 21))
    sel = "SELECT * FROM all_users;"
    dr_tb = "DROP TABLE all_users;"
    dr_db = "DROP DATABASE test_db;"

    executeSQL(st.session_state.my_cursor, c_db, st.session_state.my_db)
    executeSQL(st.session_state.my_cursor, u_db, st.session_state.my_db)
    executeSQL(st.session_state.my_cursor, c_tb, st.session_state.my_db)
    executeSQL(st.session_state.my_cursor, ins, st.session_state.my_db, vals)
    res = executeSQL(st.session_state.my_cursor, sel, fetch=True)
    for row in res:
        st.write(row)
    executeSQL(st.session_state.my_cursor, dr_tb, st.session_state.my_db)
    executeSQL(st.session_state.my_cursor, dr_db, st.session_state.my_db)

    st.session_state.my_cursor.close()
    st.session_state.my_db.close()

    st.success("Successfully executed SQL!")
