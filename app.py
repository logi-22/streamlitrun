import streamlit as st
import requests
from PIL import Image, UnidentifiedImageError
import io
import numpy as np
from transformers import AutoProcessor, CLIPModel
import logging
from pinecone import Pinecone
import streamlit as st

# Function to check authentication
def check_authentication():
    st.sidebar.title("🔑 Login")
    username = st.sidebar.text_input("Username", key="username_input")
    password = st.sidebar.text_input("Password", type="password", key="password_input")
    login_button = st.sidebar.button("Login")

    if login_button:
        try:
            stored_users = dict(st.secrets["credentials"])  # Convert to dictionary
            if username in stored_users and stored_users[username] == password:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.rerun()  # ✅ Updated method
            else:
                st.sidebar.error("❌ Invalid username or password")
        except Exception as e:
            st.sidebar.error("⚠️ Authentication system error")
            st.sidebar.text(str(e))

# Check authentication status
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    check_authentication()
    st.stop()

# Main app content (only accessible after authentication)
st.sidebar.success(f"✅ Logged in as {st.session_state['username']}")
st.title("📌 Image & Text Search using CLIP and Pinecone")
st.write("Welcome! You are successfully authenticated.")


# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load CLIP model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Initialize Pinecone
pc = Pinecone(api_key="pcsk_6QAd2e_Js1mL941ky9vvGhkGpsGmR7H8aDjKWp2vzpMiRDSvFEFGf5VT6meRJeAft1pNaE")
index_name = "images-index"

# Ensure Pinecone index exists
index_list = pc.list_indexes().names()
if index_name not in index_list:
    st.error(f"Index '{index_name}' not found. Make sure it is created.")
    st.stop()

# Initialize Pinecone index
unsplash_index = pc.Index(index_name)

def embed_text(text):
    inputs = processor(text=text, return_tensors="pt")
    text_features = model.get_text_features(**inputs)
    return text_features.detach().cpu().numpy().flatten().tolist()

def embed_image(image):
    inputs = processor(images=image, return_tensors="pt")
    image_features = model.get_image_features(**inputs)
    return image_features.detach().cpu().numpy().flatten().tolist()

# Streamlit UI
st.title("📌Image & Text Embedding Search using CLIP and Pinecone")

option = st.radio("Choose input type:", ("Text", "Image🏞️"))

if option == "Text":
    query_text = st.text_input("Enter a search term:")
    if st.button("Embed & Search"):
        if query_text:
            query_embedding = embed_text(query_text)
            search_results = unsplash_index.query(
                vector=query_embedding,
                top_k=10,
                include_metadata=True,
                namespace="image-search-dataset"
            )
            if search_results and "matches" in search_results:
                st.subheader("Search Results:")
                for match in search_results["matches"]:
                    url = match["metadata"].get("url", "No URL")
                    st.image(url, caption=f"Score: {match['score']:.4f}", use_container_width=True)
            else:
                st.warning("No matching images found.")
        else:
            st.error("Please enter a search term.")

elif option == "Image":
    uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        if st.button("Embed & Search"):
            query_embedding = embed_image(image)
            search_results = unsplash_index.query(
                vector=query_embedding,
                top_k=10,
                include_metadata=True,
                namespace="image-search-dataset"
            )
            if search_results and "matches" in search_results:
                st.subheader("Search Results:")
                for match in search_results["matches"]:
                    url = match["metadata"].get("url", "No URL")
                    st.image(url, caption=f"Score: {match['score']:.4f}", use_container_width=True)
            else:
                st.warning("No similar images found.")
