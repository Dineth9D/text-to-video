import base64
import streamlit as st
import requests

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


if option == "Text":
    prompt = st.text_area("Enter Text Prompt")
    if st.button("Generate Video"):
        with st.spinner("Generating video..."):
            response = make_request("http://localhost:8000/generate-text-video",data={"prompt": prompt, "input_type": "text"}
            )
            if response:
                try:
                    response_json = response.json()
                    # st.write(response_json)
                    video_data = response_json.get("video_url")
                    if video_data:
                        video_base64 = video_data.get("video")
                        if video_base64:
                            video_bytes = base64.b64decode(video_base64)
                            st.video(video_bytes, format="video/mp4")
                        else:
                            st.error(
                                "Failed to retrieve video: No video data in response.")
                    else:
                        st.error(
                            "Failed to retrieve video: No video_url in response.")
                except Exception as e:
                    st.error(f"Failed to retrieve video: {e}")
            else:
                st.error("Failed to retrieve video: No response from server.")


# Image input option
elif option == "Image":
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"])
    if uploaded_file and st.button("Generate Video"):
        with st.spinner("Generating video..."):
            image_bytes = uploaded_file.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            response = make_request("http://localhost:8000/generate-image-video", data={"image": image_base64, "input_type": "image"})
            if response:
                try:
                    response_json = response.json()
                    # st.write(response_json)
                    video_data = response_json.get("video_url")
                    if video_data:
                        video_base64 = video_data.get("video")
                        if video_base64:
                            video_bytes = base64.b64decode(video_base64)
                            st.video(video_bytes, format="video/mp4")
                        else:
                            st.error(
                                "Failed to retrieve video: No video data in response.")
                    else:
                        st.error(
                            "Failed to retrieve video: No video_url in response.")
                except Exception as e:
                    st.error(f"Failed to retrieve video: {e}")
            else:
                st.error("Failed to retrieve video: No response from server.")

# Text + Image input option
elif option == "Text + Image":
    prompt = st.text_area("Enter Text Prompt")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"])
    if prompt and uploaded_file and st.button("Generate Video"):
        with st.spinner("Generating video..."):
            image_bytes = uploaded_file.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            response = make_request("http://localhost:8000/generate-text-image-video", data={"prompt": prompt, "image": image_base64, "input_type": "text_image"})
            if response:
                try:
                    response_json = response.json()
                    # st.write(response_json)
                    video_data = response_json.get("video_url")
                    if video_data:
                        video_base64 = video_data.get("video")
                        if video_base64:
                            video_bytes = base64.b64decode(video_base64)
                            st.video(video_bytes, format="video/mp4")
                        else:
                            st.error(
                                "Failed to retrieve video: No video data in response.")
                    else:
                        st.error(
                            "Failed to retrieve video: No video_url in response.")
                except Exception as e:
                    st.error(f"Failed to retrieve video: {e}")
            else:
                st.error("Failed to retrieve video: No response from server.")
