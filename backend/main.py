import os
import torch
from ultralytics import YOLO
import cv2
import uuid
import io
from PIL import Image
import numpy as np
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

# Detectar si hay una GPU disponible
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Cargar el modelo YOLOv8
model = YOLO('weights/yolov8n-seg.pt')
model.to(device)  # Mover el modelo al dispositivo adecuado

# Create directories to store the original and processed images
os.makedirs('../original_images', exist_ok=True)
os.makedirs('../processed_images', exist_ok=True)

@app.get("/")
def read_root():
    return {"Hello": "You are in MyInvictIA API."}

@app.post('/detect')
async def detect_fire_ants(image: UploadFile = File(...)):
    # Read the uploaded image file
    image_bytes = await image.read()
    image = Image.open(io.BytesIO(image_bytes))

    # Determine the image format
    image_format = image.format.lower()

    # Generate a unique filename for the original and processed images
    filename = f"{uuid.uuid4()}"
    original_filename = f"{filename}_original.{image_format}"
    processed_filename = f"{filename}_processed.{image_format}"

    # Save the original image
    image.save(f"original_images/{original_filename}")

    # Realizar la detección de objetos utilizando el modelo YOLOv8
    results = model.predict(source=image, conf=0.25, device=device) # Pass the image directly as the 'source' parameter

    # Extract the detected objects and their probabilities
    detected_objects = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)
            class_name = model.names[class_id]
            confidence = float(box.conf)
            detected_objects.append({'class': class_name, 'confidence': confidence})

    # Save the processed image with RGB colors
    res_plotted = results[0].plot()
    res_plotted_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
    Image.fromarray(res_plotted_rgb).save(f"processed_images/{processed_filename}")

    return {'status': 'OK', 'detected_objects': detected_objects, 'original_filename': original_filename, 'processed_filename': processed_filename}