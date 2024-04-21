# Python code
from pathlib import Path
import sys

# Get the absolute path of the current directory
ROOT = Path().resolve()

# Sources
IMAGE = 'Image'
IMAGE_API = 'Image (API)'
VIDEO = 'Video'
WEBCAM = 'Webcam'
RTSP = 'RTSP'
YOUTUBE = 'YouTube'

SOURCES_LIST = [IMAGE, IMAGE_API, VIDEO, WEBCAM, RTSP, YOUTUBE]

# Images config
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'image_1-default.jpg'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'image_2-default.jpg'

# Videos config
VIDEO_DIR = ROOT / 'videos'
VIDEO_1_PATH = VIDEO_DIR / 'video_1.mp4'
VIDEOS_DICT = {
    'video_1': VIDEO_1_PATH
}

# ML Model config
MODEL_DIR = ROOT / 'weights'
# DETECTION_MODEL = MODEL_DIR / 'yolov8n-seg.pt'
# Uncomment the line above and comment the line below if you want to use yolov8n-seg.pt
# Place your custom model pt file name at the line below 
# DETECTION_MODEL = MODEL_DIR / 'my_detection_model.pt'

SEGMENTATION_MODEL = MODEL_DIR / 'yolov8n-seg.pt'

# Webcam
WEBCAM_PATH = 0