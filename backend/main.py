from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from s3_utils import upload_verified_image_to_s3
from tasks import process_video_task
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


class GenerateTextVideoRequest(BaseModel):
    prompt: str
    input_type: str


@app.post("/generate-text-video")
async def generate_text_video(request: GenerateTextVideoRequest):
    prompt = request.prompt
    result = process_video_task({"prompt": prompt}, "text")
    return {"message": "Video generated successfully", "video_url": result}


@app.post("/generate-image-video")
async def generate_image_video(prompt: str = Form(...), file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed.")
    
    file_content = await file.read()
    max_file_size = 5 * 1024 * 1024  # 5MB
    if len(file_content) > max_file_size:
        raise HTTPException(status_code=400, detail="File size exceeds the maximum limit of 5MB.")
    
    file_url = upload_verified_image_to_s3(file_content, file.filename)
    
    result = process_video_task(
        {"prompt": prompt, "image": file_url}, "image")
    return JSONResponse(content={"message": "Video generated successfully", "video_url": result})


@app.post("/generate-text-image-video")
async def generate_text_image_video(request: GenerateTextVideoRequest, file: UploadFile = None):
    prompt = request.prompt
    
    if file:
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed.")
        
        file_content = await file.read()
        max_file_size = 5 * 1024 * 1024  # 5MB
        if len(file_content) > max_file_size:
            raise HTTPException(status_code=400, detail="File size exceeds the maximum limit of 5MB.")
        
        file_url = upload_verified_image_to_s3(file_content, file.filename)
    else:
        file_url = None

    result = process_video_task(
        {"prompt": prompt, "image_url": file_url}, "text_image")
    return {"message": "Video generated successfully", "video_url": result}


@app.post("/status/{task_id}")
def get_task_status(task_id: str):
    return JSONResponse(content={"task_id": task_id, "status": "success"})
