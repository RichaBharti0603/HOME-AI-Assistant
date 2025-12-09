# frontend/ui/app.py
import streamlit as st
import requests

st.title("HOME — Local AI Assistant")

query = st.text_input("Ask something:")

if query:
    try:
        resp = requests.post(
            "http://127.0.0.1:8000/query",
            json={"query": query}
        ).json()
        st.write(resp.get("response", "No response received"))
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
