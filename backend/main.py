import json
from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from fastapi.responses import StreamingResponse
from s3_utils import upload_verified_image_to_s3, upload_to_s3
from tasks import process_video_task
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from tempfile import NamedTemporaryFile
import os
from typing import Optional

app = FastAPI()


class GenerateTextVideoRequest(BaseModel):
    prompt: str
    input_type: str
    image_url: Optional[str] = None


@app.post("/generate-text-video")
async def generate_text_video(request: GenerateTextVideoRequest):
    try:
        prompt = request.prompt
        input_type = request.input_type
        video_url = process_video_task({"prompt": prompt, "image_url": None}, input_type)

        #######################################################################################################
        #                                                                                                     #
        #  Uncomment the following code and remove the pass statements if you want to upload the video to S3  #
        #                                                                                                     #
        #######################################################################################################

        # with NamedTemporaryFile(delete=False) as temp_file:
        #     temp_file.write(video_content)
        #     temp_file_path = temp_file.name

        try:

            # video_url = upload_to_s3(temp_file_path, "generated_text_video.mp4")
            pass
        finally:
            # os.remove(temp_file_path)
            pass
        
        return {"message": "Video generated successfully", "video_url": video_url}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"An error occurred: {str(e)}"})


@app.post("/generate-image-video")
async def generate_image_video( file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed.")

    file_content = await file.read()
    max_file_size = 5 * 1024 * 1024  # 5MB
    if len(file_content) > max_file_size:
        raise HTTPException(
            status_code=400, detail="File size exceeds the maximum limit of 5MB.")

    # Uncomment the following line and remove assign the file_url to the uploaded image URL
    # file_url = upload_verified_image_to_s3(file_content, file.filename)
    file_url = "https://github.com/Dineth9D/text-to-video/blob/main/backend/rb_35017.png"

    video_content = process_video_task(
        {"image_url": file_url}, "image")

    #######################################################################################################
    #                                                                                                     #
    #  Uncomment the following code and remove the pass statements if you want to upload the video to S3  #
    #                                                                                                     #
    #######################################################################################################

    # with NamedTemporaryFile(delete=False) as temp_file:
    #     temp_file.write(video_content)
    #     temp_file_path = temp_file.name

    try:
        # video_url = upload_to_s3(temp_file_path, "generated_image_video.mp4")
        pass
    finally:
        # os.remove(temp_file_path)
        pass

    # USe video_url instead of video_content if you want to return the URL of the video
    return {"message": "Video generated successfully", "video_url": video_content}


@app.post("/generate-text-image-video")
async def generate_text_image_video(request: str = Form(...), file: UploadFile = None):
    request_data = json.loads(request)
    prompt = request_data['prompt']

    if file:
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed.")

        file_content = await file.read()
        max_file_size = 5 * 1024 * 1024  # 5MB
        if len(file_content) > max_file_size:
            raise HTTPException(
                status_code=400, detail="File size exceeds the maximum limit of 5MB.")
            
        # Uncomment the following line and remove assign the file_url to the uploaded image URL
        # file_url = upload_verified_image_to_s3(file_content, file.filename)
        file_url = "https://github.com/Dineth9D/text-to-video/blob/main/backend/rb_35017.png"
    else:
        file_url = None

    video_content = process_video_task(
        {"prompt": prompt, "image_url": file_url}, "text_image")

    #######################################################################################################
    #                                                                                                     #
    #  Uncomment the following code and remove the pass statements if you want to upload the video to S3  #
    #                                                                                                     #
    #######################################################################################################

    # with NamedTemporaryFile(delete=False) as temp_file:
    #     temp_file.write(video_content)
    #     temp_file_path = temp_file.name

    try:
        # video_url = upload_to_s3(temp_file_path, "generated_text_image_video.mp4")
        pass
    finally:
        # os.remove(temp_file_path)
        pass

    # USe video_url instead of video_content if you want to return the URL of the video
    return {"message": "Video generated successfully", "video_url": video_content}


@app.post("/status/{task_id}")
def get_task_status(task_id: str):
    return JSONResponse(content={"task_id": task_id, "status": "success"})
