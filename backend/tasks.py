from models import generate_video
from s3_utils import upload_to_s3


def process_video_task(input_data, input_type):
    prompt = input_data["prompt"]
    image_url = input_data["image_url"]
    url = input_data["ngrok_url"]
    output_file = generate_video(prompt, image_url, input_type, url)
    
    # output_path = "https://www.sample-videos.com/video321/mp4/720/big_buck_bunny_720p_2mb.mp4"
    
    # # Upscale the generated video
    # upscale_video = upscale_video_task(output_path)
    
    # # Upscale the generated video
    # output_path = upload_to_s3(output_path)
    return output_file


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