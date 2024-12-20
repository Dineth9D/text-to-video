from celery import Celery
from models import generate_video
from s3_utils import upload_to_s3
# from realesrgan import RealESRGAN
import cv2
import os
import subprocess


def process_video_task(input_data, input_type):
    prompt = input_data["prompt"]
    image_url = input_data["image_url"]
    output_path = generate_video(prompt, image_url, input_type)
    
    # # Upscale the generated video
    # upscale_video = upscale_video_task(output_path)
    
    # # Upscale the generated video
    # video_url = upload_to_s3(output_path)
    return output_path


# def upscale_video_task(input_path):
#     model = RealESRGAN("RealESRGAN_x4plusts", scale=4)
#     model.load_model()

#     cap = cv2.VideoCapture(input_path)
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = int(cap.get(cv2.CAP_PROP_FPS))

#     upscale_output_path = input_path.replace(".mp4", "_upscaled.mp4")
#     out = cv2.VideoWriter(upscale_output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width * 4, frame_height * 4))

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         upscaled_frame = model.enhance(frame)
#         out.write(upscaled_frame)

#     cap.release()
#     out.release()
#     return upscale_output_path