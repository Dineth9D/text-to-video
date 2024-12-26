import streamlit as st
import requests
import json

st.title("Text-to-Video Generation System")

option = st.selectbox("Select Input Type", ["Text", "Image", "Text + Image"])


def make_request(url, data=None, files=None):
    try:
        if files:
            response = requests.post(url, data=data, files=files)
        else:
            response = requests.post(url, json=data)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None


# Text input option
if option == "Text":
    prompt = st.text_area("Enter Text Prompt")
    if st.button("Generate Video"):
        with st.spinner("Generating video..."):
            response = make_request(
                "http://localhost:8000/generate-text-video",
                data={"prompt": prompt, "input_type": "text"}
            )
            if response:
                response_json = response.json()
                video_url = response_json.get("video_url")
                st.video(video_url, format="video/mp4")
            else:
                st.error("Failed to retrieve video.")

# Image input option
elif option == "Image":
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"])
    if uploaded_file and st.button("Generate Video"):
        with st.spinner("Generating video..."):
            files = {"file": uploaded_file}
            response = make_request(
                "http://localhost:8000/generate-image-video", files=files)
            if response:
                response_json = response.json()
                video_url = response_json.get("video_url")
                st.video(video_url, format="video/mp4")
            else:
                st.error("Failed to retrieve video.")

# Text + Image input option
elif option == "Text + Image":
    prompt = st.text_area("Enter Text Prompt")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"])
    if prompt and uploaded_file and st.button("Generate Video"):
        with st.spinner("Generating video..."):
            files = {"file": (uploaded_file.name,
                              uploaded_file.getvalue(), uploaded_file.type)}
            data = {"prompt": prompt}
            response = make_request(
                "http://localhost:8000/generate-text-image-video",
                data={"request": json.dumps(data)},
                files=files
            )
            if response:
                response_json = response.json()
                video_url = response_json.get("video_url")
                st.video(video_url, format="video/mp4")
            else:
                st.error("Failed to retrieve video.")

# Task status section
st.write("Check Task Status:")
task_id = st.text_input("Enter Task ID")
if st.button("Get Status"):
    with st.spinner("Fetching status..."):
        try:
            status_response = requests.get(
                f"http://localhost:8000/status/{task_id}")
            status_response.raise_for_status()
            status_data = status_response.json()
            st.json(status_data)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
