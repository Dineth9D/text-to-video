from gradio_client import Client, handle_file
from decouple import config

HUGGINGFACE_API_KEY = config("HUGGINGFACE_API_KEY")


def generate_video(prompt, image_url, input_type):
    if input_type == "text":
        client = Client("Moupiya/texttovideo", hf_token = HUGGINGFACE_API_KEY)
        video_path = client.predict(
            prompt=prompt,
            negative_prompt=prompt,
            num_frames=16,
            guidance_scale=2,
            num_inference_steps=6,
            seed=0,
            api_name="/predict"
        )

    elif input_type == "image":
        client = Client("Moupiya/texttovideo", hf_token = HUGGINGFACE_API_KEY)
        video_path = client.predict(
            prompt=prompt,
            negative_prompt=prompt,
            num_frames=16,
            guidance_scale=2,
            num_inference_steps=6,
            seed=0,
            api_name="/predict"
        )

    elif input_type == "text_image":
        client = Client("peterpeter8585/image-to-video-cog", hf_token = HUGGINGFACE_API_KEY)
        video_path = client.predict(
            prompt=prompt,
            image=handle_file(image_url),
            api_name="/generate_video"
        )

    return video_path
