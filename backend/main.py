import json
from typing import Optional

from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from s3_utils import upload_verified_image_to_s3, upload_to_s3
from tasks import process_video_task

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

    video_url = process_video_task(
        {"image_url": file_url}, "image")

    return {"message": "Video generated successfully", "video_url": video_url}


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

    video_url = process_video_task(
        {"prompt": prompt, "image_url": file_url}, "text_image")

    return {"message": "Video generated successfully", "video_url": video_url}


@app.post("/status/{task_id}")
def get_task_status(task_id: str):
    return JSONResponse(content={"task_id": task_id, "status": "success"})
