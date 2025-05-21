import streamlit as st
import json
import os
from pathlib import Path

USER_DB = Path(__file__).parent.parent / "data/users.json"

def load_users():
    if not USER_DB.exists():
        USER_DB.parent.mkdir(exist_ok=True, parents=True)
        with open(USER_DB, "w") as f:
            json.dump({}, f)
    try:
        with open(USER_DB, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

def add_user(username, password):
    if not username or not password:
        return "empty"
    users = load_users()
    if username in users:
        return "exists"
    users[username] = password  # In production, use proper password hashing
    save_users(users)
    return "ok"

def authenticate(username, password):
    users = load_users()
    return users.get(username) == password

def login_user():
    if st.session_state.authenticated:
        return True

    st.subheader("🔐 Login or Register")
    action = st.selectbox("Choose action", ["Login", "Register"], key="auth_action")

    with st.form("auth_form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button(action)

        if submitted:
            if not username or not password:
                st.error("Please enter both username and password.")
                return False
            if action == "Login":
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.rerun()
                    return True
                else:
                    st.error("Invalid credentials")
                    return False
            elif action == "Register":
                res = add_user(username, password)
                if res == "exists":
                    st.error("Username already exists")
                elif res == "empty":
                    st.error("Cannot use empty credentials")
                else:
                    st.success("Registration successful! Please login")
                return False

    return False

def logout_user():
    st.session_state.authenticated = False
    st.session_state.username = ""