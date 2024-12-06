from celery import Celery
from models import generate_video
# from s3_utils import upload_to_s3
# from realesrgan import RealESRGAN
import cv2


def process_video_task(input_data, input_type):
    prompt = input_data["prompt"]
    image_url = input_data["image_url"]
    output_path = generate_video(prompt, image_url, input_type)
    # video_url = upload_to_s3(output_path)
    return output_path