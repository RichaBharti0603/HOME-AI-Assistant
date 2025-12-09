import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import streamlit as st
from backend.rag.rag import answer_query
st.title("HOME — Local AI Assistant")
query = st.text_input("Ask something:")
if query:
    resp = answer_query(query)
    st.write(resp)
