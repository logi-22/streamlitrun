import streamlit as st
import requests
from PIL import Image
import io

# FastAPI backend URL
BACKEND_URL = "http://0.0.0.0:8000"

st.title("📌 Image & Text Search using CLIP and Pinecone")

option = st.radio("Choose input type:", ("Text", "Image"))

if option == "Text":
    query_text = st.text_input("Enter a search term:")
    if st.button("Search"):
        if query_text:
            response = requests.post(f"{BACKEND_URL}/embed_text", data={"query": query_text})
            if response.status_code == 200:
                results = response.json().get("results", [])
                st.subheader("Search Results:")
                for match in results:
                    url = match["metadata"].get("url", "No URL")
                    st.image(url, caption=f"Score: {match['score']:.4f}", use_container_width=True)
            else:
                st.warning("No matches found.")
        else:
            st.error("Please enter a search term.")

elif option == "Image":
    uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        if st.button("Search"):
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(f"{BACKEND_URL}/embed_image", files=files)
            if response.status_code == 200:
                results = response.json().get("results", [])
                st.subheader("Search Results:")
                for match in results:
                    url = match["metadata"].get("url", "No URL")
                    st.image(url, caption=f"Score: {match['score']:.4f}", use_container_width=True)
            else:
                st.warning("No matches found.")
