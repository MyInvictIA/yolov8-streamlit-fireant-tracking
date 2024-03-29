from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse  # Añade esta línea
import os
import torch
import numpy as np
from PIL import Image
import cv2
from ultralytics import YOLO
import aiofiles
from datetime import datetime
import io

app = FastAPI()

app.mount("/processed_videos", StaticFiles(directory="/app/processed_videos"), name="processed_videos")


@app.get("/processed_videos/{processed_filename}")  # Añade esta ruta
async def get_video(processed_filename: str):
    processed_video_path = f"/app/processed_videos/{processed_filename}"
    return FileResponse(processed_video_path, media_type="video/mp4")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = YOLO('weights/yolov8x-seg.pt')
model.to(device)

os.makedirs('/app/original_images', exist_ok=True)
os.makedirs('/app/processed_images', exist_ok=True)
os.makedirs('/app/original_videos', exist_ok=True)
os.makedirs('/app/processed_videos', exist_ok=True)


@app.get("/")
def read_root():
    return {"Hello": "You are in MyInvictIA API. Version v0.1"}


@app.post('/detect_img')
async def detect_fire_ants_in_image(image: UploadFile = File(...)):
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Separate filename and extension
    original_name, original_ext = os.path.splitext(image.filename)
    # Cleaning the filename
    cleaned_filename = "".join(x for x in original_name if x.isalnum() or x in "._")
    # Defining the original and processed filenames
    original_filename = f"{cleaned_filename}_{now}_original{original_ext}"
    processed_filename = f"{cleaned_filename}_{now}_processed.jpg"

    image_bytes = await image.read()

    async with aiofiles.open(f"/app/original_images/{original_filename}", "wb") as f:
        await f.write(image_bytes)

    with Image.open(io.BytesIO(image_bytes)).convert('RGB') as image:
        results = model.track(image, conf=0.25)

    detected_objects = []
    for result in results:
        for box in result.boxes:
            object_id = box.id if 'id' in box else None
            detected_objects.append({
                'class': model.names[box.cls.cpu().numpy().item()],
                'confidence': box.conf.cpu().numpy().item(),
                'id': object_id,
            })

    res_plotted = results[0].plot()
    res_plotted_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(res_plotted_rgb)

    async with aiofiles.open(f"/app/processed_images/{processed_filename}", "wb") as f:
        pil_image.save(f, format='JPEG')

    return {'status': 'OK',
            'detected_objects': detected_objects,
            'original_filename': original_filename,
            'processed_filename': processed_filename}


@app.post('/detect_video')
async def detect_fire_ants_in_video(video: UploadFile = File(...)):
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    original_name, original_ext = os.path.splitext(video.filename)
    cleaned_filename = "".join(x for x in original_name if x.isalnum() or x in "._")
    original_filename = f"{cleaned_filename}_{now}_original{original_ext}"
    processed_filename = f"{cleaned_filename}_{now}_processed.mp4"

    video_bytes = await video.read()
    async with aiofiles.open(f"/app/original_videos/{original_filename}", "wb") as f:
        await f.write(video_bytes)

    video_path = f"/app/original_videos/{original_filename}"
    processed_video_path = f"/app/processed_videos/{processed_filename}"

    cap = cv2.VideoCapture(video_path)
    frames = []
    detected_objects = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.track(frame, conf=0.25)
        for result in results:
            for box in result.boxes:
                object_id = box.id if 'id' in box else None
                detected_objects.append({
                    'class': model.names[box.cls.cpu().numpy().item()],
                    'confidence': box.conf.cpu().numpy().item(),
                    'id': object_id,
                })

        res_plotted = results[0].plot()
        frame_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
        frames.append(frame_rgb)

    cap.release()
    out = cv2.VideoWriter(processed_video_path, cv2.VideoWriter_fourcc(*'mp4v'), 20,
                          (frames[0].shape[1], frames[0].shape[0]))

    for frame in frames:
        out.write(frame)
    out.release()

    processed_video_url = f"http://localhost:8000/processed_videos/{processed_filename}"

    return {'status': 'OK',
            'detected_objects': detected_objects,
            'original_filename': original_filename,
            'processed_video_url': processed_video_url}
