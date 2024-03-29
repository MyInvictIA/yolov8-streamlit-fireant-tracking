from pathlib import Path
import sys

# Get the absolute path of the current file
file_path = Path(__file__).resolve()

# Get the parent directory of the current file
root_path = file_path.parent

# Add the root path to the sys.path list if it is not already there
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Get the relative path of the root directory with respect to the current working directory
ROOT = root_path.relative_to(Path.cwd())

# Sources
IMAGE = 'Image'
VIDEO = 'Video'
WEBCAM = 'Webcam'
RTSP = 'RTSP'
YOUTUBE = 'YouTube'

SOURCES_LIST = [IMAGE, VIDEO, WEBCAM, RTSP, YOUTUBE]

# Images config
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'image_1.jpg'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'image_2.jpg'

# Videos config
VIDEO_DIR = ROOT / 'videos'
VIDEO_1_PATH = VIDEO_DIR / 'video_1.mp4'
VIDEOS_DICT = {
    'video_1': VIDEO_1_PATH
}

# ML Model config
MODEL_DIR = ROOT / 'weights'
#DETECTION_MODEL = MODEL_DIR / 'yolov8n.pt'
# In case of your custom model comment out the line above and
# Place your custom model pt file name at the line below 
# DETECTION_MODEL = MODEL_DIR / 'my_detection_model.pt'

SEGMENTATION_MODEL = MODEL_DIR / 'yolov8x-seg.pt'

# Webcam
WEBCAM_PATH = 0

# Class indices for YOLOv8 detection
ANTHILL_CLASS_INDEX = 0   # Modifica este valor si tu modelo usa un índice diferente para hormigueros
ANT_CLASS_INDEX = 1  # Modifica este valor si tu modelo usa un índice diferente para hormigas
