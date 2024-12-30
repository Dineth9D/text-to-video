import json
from typing import Optional

from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from tasks import process_video_task

app = FastAPI()


class GenerateTextVideoRequest(BaseModel):
    prompt: Optional[str] = None
    input_type: str
    image: Optional[str] = None


@app.post("/generate-text-video")
async def generate_text_video(request: GenerateTextVideoRequest):
    try:
        prompt = request.prompt
        input_type = request.input_type
        video_url = process_video_task(
            {"prompt": prompt, "image_url": None}, input_type)

        return {"message": "Video generated successfully", "video_url": video_url}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"An error occurred: {str(e)}"})


@app.post("/generate-image-video")
async def generate_image_video(request: GenerateTextVideoRequest):
    try:
        image = request.image
        input_type = request.input_type
        video_url = process_video_task(
            {"prompt": None, "image_url": image}, input_type)

        return {"message": "Video generated successfully", "video_url": video_url}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"An error occurred: {str(e)}"})


@app.post("/generate-text-image-video")
async def generate_text_image_video(request: GenerateTextVideoRequest):
    try:
        prompt = request.prompt
        image = request.image
        video_url = process_video_task(
            {"prompt": prompt, "image_url": image}, "text_image")

        return {"message": "Video generated successfully", "video_url": video_url}

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"An error occurred: {str(e)}"})
