import streamlit as st
import requests
from PIL import Image
import io
import json

# API Base URL
API_URL = "http://0.0.0.0:7860"

# Authentication
st.sidebar.title("🔑 Login")
username = st.sidebar.text_input("Username", key="username_input")
password = st.sidebar.text_input("Password", type="password", key="password_input")
login_button = st.sidebar.button("Login")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if login_button:
    try:
        response = requests.post(
            f"{API_URL}/embed_text/", data={"text": "test"}, auth=(username, password)
        )
        if response.status_code == 200:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid credentials")
    except Exception as e:
        st.sidebar.error("⚠️ Authentication error")
        st.sidebar.text(str(e))

if not st.session_state["authenticated"]:
    st.stop()

st.title("📌 Image & Text Search with CLIP and Pinecone")
option = st.radio("Choose input type:", ("Text", "Image"))

if option == "Text":
    query_text = st.text_input("Enter a search term:")
    if st.button("Search"):
        if query_text:
            response = requests.post(
                f"{API_URL}/embed_text/", data={"text": query_text}, auth=(username, password)
            )
            if response.status_code == 200:
                embedding = response.json()["embedding"]
                search_response = requests.post(
                    f"{API_URL}/search/", json={"query_embedding": embedding}, auth=(username, password)
                )
                results = search_response.json().get("results", [])
                if results:
                    for match in results:
                        url = match["metadata"].get("url", "No URL")
                        st.image(url, caption=f"Score: {match['score']:.4f}", use_container_width=True)
                else:
                    st.warning("No matching images found.")
            else:
                st.error("Error retrieving embedding.")
        else:
            st.error("Please enter a search term.")

elif option == "Image":
    uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        if st.button("Search"):
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format="PNG")
            img_byte_arr = img_byte_arr.getvalue()
            files = {"file": (uploaded_file.name, img_byte_arr, "image/png")}
            response = requests.post(f"{API_URL}/embed_image/", files=files, auth=(username, password))
            if response.status_code == 200:
                embedding = response.json()["embedding"]
                search_response = requests.post(
                    f"{API_URL}/search/", json={"query_embedding": embedding}, auth=(username, password)
                )
                results = search_response.json().get("results", [])
                if results:
                    for match in results:
                        url = match["metadata"].get("url", "No URL")
                        st.image(url, caption=f"Score: {match['score']:.4f}", use_container_width=True)
                else:
                    st.warning("No similar images found.")
            else:
                st.error("Error retrieving embedding.")
