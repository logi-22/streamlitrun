import streamlit as st
import requests
import os

# Backend API URL
API_URL = "https://logeswari-new-1.hf.space"

# Session state for authentication
if "access_token" not in st.session_state:
    st.session_state.access_token = None

st.title("🔍 Image Search System")
st.sidebar.subheader("Login")

# Login form
with st.sidebar.form(key="login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button("Login")

    if submit_button:
        response = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
        if response.status_code == 200:
            st.session_state.access_token = response.json().get("access_token")
            st.sidebar.success("✅ Logged in successfully!")
        else:
            st.sidebar.error("❌ Incorrect username or password")

# Check authentication
if not st.session_state.access_token:
    st.warning("🔒 Please log in first.")
    st.stop()

# Tabs for text search and image search
tab1, tab2 = st.tabs(["🔠 Search by Text", "🖼️ Search by Image"])

# Text-based search
with tab1:
    st.subheader("🔠 Search by Text")
    text_query = st.text_input("Enter a search query:")
    if st.button("🔍 Search"):
        if text_query:
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
            response = requests.get(f"{API_URL}/search/text/", params={"query": text_query}, headers=headers)

            if response.status_code == 200:
                results = response.json().get("matches", [])
                if results:
                    st.success(f"✅ Found {len(results)} similar images!")
                    for match in results:
                        st.image(match["url"], caption=f"Match ID: {match['id']} - Score: {match['score']:.4f}")
                else:
                    st.warning("❌ No matches found.")
            else:
                st.error("⚠️ Error searching for images.")

# Image-based search
with tab2:
    st.subheader("🖼️ Search by Image")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if st.button("🔍 Search by Image") and uploaded_file:
        files = {"file": uploaded_file.getvalue()}
        headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
        response = requests.post(f"{API_URL}/search/image/", files=files, headers=headers)

        if response.status_code == 200:
            results = response.json().get("matches", [])
            if results:
                st.success(f"✅ Found {len(results)} similar images!")
                for match in results:
                    st.image(match["url"], caption=f"Match ID: {match['id']} - Score: {match['score']:.4f}")
            else:
                st.warning("❌ No matches found.")
        else:
            st.error("⚠️ Error searching for images.")

st.sidebar.button("Logout", on_click=lambda: st.session_state.pop("access_token", None))
