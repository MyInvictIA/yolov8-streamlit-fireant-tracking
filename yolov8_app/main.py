# Python In-built packages
import os
from datetime import datetime

# External Packages
import aiofiles
from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
import cv2
import torch
from ultralytics import YOLO
import io

app = FastAPI()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = YOLO('weights/yolov8n-seg.pt')
model.to(device)

os.makedirs('./images', exist_ok=True)
os.makedirs('./images/processed', exist_ok=True)
os.makedirs('./images/original', exist_ok=True)


@app.get("/")
def read_root():
    return {"Hello": "You are in MyInvictIA API. Version v0.2"}


@app.post('/detect_img')
async def display_detected_frames(image: UploadFile = File(...), filename: str = Form(None)):
    # Get the current date and time
    now = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Default filename if no filename is provided
    filename = filename if filename else image.filename if image.filename and image.filename != 'image' else f"default_image_{now}"
    # Separate filename and extension
    original_name, original_extension = os.path.splitext(filename)

    # If no extension is provided, default to .jpg
    if not original_extension:
        original_extension = ".jpg"

    # Cleaning the filename
    cleaned_filename = "".join(x for x in original_name if x.isalnum() or x in "._")

    # Defining the original and processed filenames
    original_filename = f"{cleaned_filename}_original{original_extension}"
    processed_filename = f"{cleaned_filename}_processed.jpg"

    image_bytes = await image.read()

    async with aiofiles.open(f"./images/original/{original_filename}", "wb") as f:
        await f.write(image_bytes)

    with Image.open(io.BytesIO(image_bytes)).convert('RGB') as image:
        results = model.track(image, conf=0.25)

    detected_objects = []
    for result in results:
        for box in result.boxes:
            object_id = box.id if 'id' in box else None
            detected_objects.append({
                'class': model.names[box.cls.cpu().numpy().item()],
                'confidence': box.conf.cpu().numpy().item()
            })

    res_plotted = results[0].plot()
    res_plotted_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(res_plotted_rgb)

    with open(f"./images/processed/{processed_filename}", "wb") as f:
        pil_image.save(f, format='JPEG')

    return {'status': 'OK',
            'detected_objects': detected_objects,
            'original_filename': original_filename,
            'processed_filename': processed_filename}