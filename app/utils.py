import streamlit as st
import json
import os
import re
import bcrypt
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

def is_valid_username(username):
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_]{3,15}$", username))  # starts with letter, 4–16 chars

def is_valid_password(password):
    return (
        len(password) >= 6 and
        re.search(r"[0-9]", password)
    )

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def add_user(username, password):
    if not is_valid_username(username):
        return "invalid_username"
    if not is_valid_password(password):
        return "invalid_password"

    users = load_users()
    if username in users:
        return "exists"

    users[username] = hash_password(password)
    save_users(users)
    return "ok"

def authenticate(username, password):
    users = load_users()
    hashed = users.get(username)
    if not hashed:
        return False
    return verify_password(password, hashed)

def login_user():
    if st.session_state.get("authenticated"):
        return True

    st.subheader("🔐 Login or Register")
    action = st.selectbox("Choose action", ["Login", "Register", "Forgot Password"], key="auth_action")

    with st.form("auth_form", clear_on_submit=True):
        username = st.text_input("Username")

        if action == "Forgot Password":
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
        else:
            password = st.text_input("Password", type="password")

        submitted = st.form_submit_button(action)

        if submitted:
            if not username:
                st.error("Please enter your username.")
                return False

            if action == "Login":
                if not password:
                    st.error("Enter your password.")
                    return False
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.rerun()
                    return True
                else:
                    st.error("Invalid credentials")
                    return False

            elif action == "Register":
                if not password:
                    st.error("Enter your password.")
                    return False
                res = add_user(username, password)
                if res == "exists":
                    st.error("Username already exists")
                elif res == "invalid_username":
                    st.error("Username must start with a letter and be 4–16 characters long.")
                elif res == "invalid_password":
                    st.error("Password must be at least 6 characters long, with uppercase, lowercase, and a number.")
                else:
                    st.success("Registration successful! Please login.")
                return False

            elif action == "Forgot Password":
                users = load_users()
                if username not in users:
                    st.error("Username not found.")
                    return False
                if new_password != confirm_password:
                    st.error("Passwords do not match.")
                    return False
                if not is_valid_password(new_password):
                    st.error("Password must be at least 6 characters long, with uppercase, lowercase, and a number.")
                    return False
                users[username] = hash_password(new_password)
                save_users(users)
                st.success("Password reset successful! Please login.")
                return False

def logout_user():
    st.session_state.authenticated = False
    st.session_state.username = ""
