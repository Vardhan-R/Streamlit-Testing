from sqlalchemy import create_engine, Engine, text, TextClause
from sqlalchemy.orm import Session
import random
import streamlit as st

def executeSQL(stmt: TextClause, engine: Engine, commit: bool = False, params: list[dict] | None = None):
    with Session(engine) as session:
        res = session.execute(stmt, params)

        if commit:
            session.commit()

    # with engine.begin() as conn:
    #     res = conn.execute(stmt, params)

    return res

if "engine" not in st.session_state:
    # st.session_state.engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    st.session_state.engine = create_engine("sqlite+pysqlite:///pages/common/databases/my_db_1.db", echo=True)

if st.button("Execute SQL"):
    # sql = "CREATE TABLE my_table_1 (temperature int, intensity int)"
    # params = None
    # res = executeSQL(text(sql), st.session_state.engine, True, params)

    sql = "INSERT INTO my_table_1 VALUES (:x, :y)"
    params = [{"x": random.randint(1, 10), "y": random.randint(1, 10)}]
    res = executeSQL(text(sql), st.session_state.engine, True, params)

    sql = "SELECT * FROM my_table_1"
    params = None
    res = executeSQL(text(sql), st.session_state.engine, False, params)

    # sql = "DELETE FROM my_table_1 WHERE 1"
    # # sql = "DROP TABLE my_table_1"
    # # sql = "PRAGMA database_list"
    # # # sql = "PRAGMA table_info"
    # params = None
    # res = executeSQL(text(sql), st.session_state.engine, True, params)

    try:
        for row in res:
            st.write(row)
    except:
        pass
    st.success(f'Successfully executed "{sql}"')
