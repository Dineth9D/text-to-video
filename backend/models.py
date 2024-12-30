import base64
import uuid
import logging
import requests
from requests.adapters import HTTPAdapter
from requests.adapters import Retry


def generate_video(prompt, image_base64, input_type, url):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    request_id = str(uuid.uuid4())
    payload = {"request_id": request_id}

    if input_type == "text":
        payload["text"] = prompt
    elif input_type == "image":
        payload["image"] = image_base64

    elif input_type == "text_image":
        payload["text"] = prompt
        payload["image"] = image_base64
    else:
        raise ValueError("Invalid input type. Must be 'text', 'image', or 'text_image'.")

    # logger.debug(f"Payload: {payload}")

    try:
        session = requests.Session()
        # retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        # session.mount("https://", HTTPAdapter(max_retries=retries))
        
        headers = {
            'Connection': 'keep-alive'
        }


        response = session.post(url, json=payload, headers= headers, timeout=1200)
        response.raise_for_status()

        video_base64 = base64.b64encode(response.content).decode('utf-8')

        response_data = {
            "video": video_base64,
            "filename": f"{request_id}.mp4"
        }

        return response_data

    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
        return None
