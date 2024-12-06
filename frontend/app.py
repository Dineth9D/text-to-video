import streamlit as st
import requests

st.title("Text-to-Video Generation System")

option = st.selectbox("Select Input Type", ["Text", "Image", "Text + Image"])

if option == "Text":
    prompt = st.text_area("Enter Text Prompt")
    if st.button("Generate Video"):
        response = requests.post("http://localhost:8000/generate-text-video", json={"prompt": prompt, "input_type": "text"})
        st.json(response.json())

elif option == "Image":
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"])
    if uploaded_file and st.button("Generate Video"):
        files = {"file": uploaded_file}
        response = requests.post("http://localhost:8000/generate-image-video", files=files)
        st.json(response.json())

elif option == "Text + Image":
    prompt = st.text_area("Enter Text Prompt")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"])
    if prompt and uploaded_file and st.button("Generate Video"):
        files = {"file": uploaded_file}
        data = {"prompt": prompt}
        response = requests.post("http://localhost:8000/generate-text-image-video", data=data, files=files)
        st.json(response.json())

st.write("Check Task Status:")
task_id = st.text_input("Enter Task ID")
if st.button("Get Status"):
    status_response = requests.get(f"http://localhost:8000/status/{task_id}")
    st.json(status_response.json())
