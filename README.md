---
title: Indexing
emoji: 🌍
colorFrom: indigo
colorTo: green
sdk: streamlit
sdk_version: 1.42.2
app_file: app.py
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference


# 📌 Image & Text Embedding Search using CLIP and Pinecone  

This project is a **Streamlit-based web application** that enables **image and text-based searches** using OpenAI's CLIP model and Pinecone for vector storage and retrieval.

## 🚀 Features  
- **Text-to-Image Search**: Enter a text query to find similar images from the dataset.  
- **Image-to-Image Search**: Upload an image to find visually similar images.  
- **CLIP Model for Embeddings**: Uses `openai/clip-vit-base-patch32` to generate embeddings for text and images.  
- **Pinecone Vector Search**: Stores and retrieves image embeddings efficiently.  
- **Interactive UI**: Built with Streamlit for easy access and visualization.  

## 🛠️ Installation  

### 1️⃣ Clone the Repository  
```sh
git clone https://github.com/your-username/image-text-search.git
cd image-text-search


flowchart TD
    A[User Input] -->|Text Query| B[Embed Text with CLIP]
    A -->|Upload Image| C[Embed Image with CLIP]
    B --> D[Query Pinecone Index]
    C --> D
    D --> E[Retrieve Top-k Similar Images]
    E --> F[Display Results in Streamlit UI]
