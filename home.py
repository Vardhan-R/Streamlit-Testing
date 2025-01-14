import os
import streamlit as st

st.set_page_config("Testing")
st.title("Testing")

pages = os.listdir("./pages")
for page in pages:
    if page.endswith(".py"):
        st.page_link(os.path.join("./pages", page))
