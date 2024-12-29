import base64
import uuid
import requests
from requests.adapters import HTTPAdapter
from requests.adapters import Retry


def generate_video(prompt, image_url, input_type):
    url = "https://7e1f-34-126-138-214.ngrok-free.app/predict/"
    request_id = str(uuid.uuid4())
    payload = {"request_id": request_id}

    if input_type == "text":
        payload["text"] = prompt
    elif input_type == "image":
        payload["image_url"] = image_url
    elif input_type == "text_image":
        payload["text"] = prompt
        payload["image_url"] = image_url
    else:
        raise ValueError(
            "Invalid input type. Must be 'text', 'image', or 'text_image'.")

    try:
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=1,
                        status_forcelist=[500, 502, 503, 504])
        session.mount("https://", HTTPAdapter(max_retries=retries))

        response = session.post(url, json=payload)
        response.raise_for_status()

        # video_filename = f"{request_id}.mp4"
        # with open(video_filename, "wb") as video_file:
        #     video_file.write(response.content)

        video_base64 = base64.b64encode(response.content).decode('utf-8')

        response_data = {
            "video": video_base64,
            "filename": f"{request_id}.mp4"
        }

        print(f"Video encoded and sent to frontend")
        return response_data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
