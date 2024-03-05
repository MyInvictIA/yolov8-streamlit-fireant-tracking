# Real-time Object Detection and Tracking with YOLOv8 and Streamlit

Web Application using YOLOv8 algorithm for object detection and segmentation in pair with Streamlit framework for Real-Time Object Detection and tracking in video streams.

## Demo WebApp

This app is up and running on Streamlit cloud server!!! Thanks 'Streamlit' for the community support for the cloud upload. You can check the demo of this web application on the link below.

[yolov8-streamlit-detection-tracking-webapp]()

## Tracking With Object Detection Demo

To be uploaded..

## Demo Pics

### Home page

To be uploaded..

### Page after uploading an image and object detection

To be uploaded..

### Segmentation task on image

To be uploaded..

## Requirements

- Python 3.8.10
- YOLOv8 (Ultralytics)
- Streamlit
- PyTorch
- lapx
- pytube

```bash
pip install ultralytics streamlit pafy
pip install pytube lapx
```

## Installation

- Clone the repository: git clone <https://github.com/MyInvictIA/yolov8-streamlit-fireant-tracking.git>
- Change to the repository directory: `cd yolov8-streamlit-fireant-tracking`
- Upgrade PIP
```bash
python -m pip install --upgrade pip
```
- For PyTorch select your custom options of your computer following the [official page](https://pytorch.org/get-started/locally/).
  - For example, for a Windows PC with NVIDIA:

    ```bash
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    ```

## Usage

- Run the app with the following command:
```bash
streamlit run app.py
```
- The app should open in a new browser window.
- We are now inside the image detection page.

### ML Model Config

- Select task (Segmentation)
- Select model confidence
- Use the slider to adjust the confidence threshold (25-100) for the model.

One the model config is done, select a source.

### Detection on images

- The default image with its objects-detected image is displayed on the main page.
- Select a source. (radio button selection `Image`, can be used for Local or images from Internet).
- Upload an image by clicking on the "Browse files" button.
- Click the "Detect Objects" button to run the object detection algorithm on the uploaded image with the selected confidence threshold.
- The resulting image with objects detected will be displayed on the page. Click the "Download Image" button to download the image.("If save image to download" is selected)

## Detection in Videos

- Create a folder with name `videos` in the same directory
- Dump your videos in this folder
- In `settings.py` edit the following lines.

```python
# video
VIDEO_DIR = ROOT / 'videos' # After creating the videos folder

# Suppose you have four videos inside videos folder
# Edit the name of video_1, 2, 3, 4 (with the names of your video files) 
VIDEO_1_PATH = VIDEO_DIR / 'video_1.mp4' 
VIDEO_2_PATH = VIDEO_DIR / 'video_2.mp4'
VIDEO_3_PATH = VIDEO_DIR / 'video_3.mp4'
VIDEO_4_PATH = VIDEO_DIR / 'video_4.mp4'

# Edit the same names here also.
VIDEOS_DICT = {
    'video_1': VIDEO_1_PATH,
    'video_2': VIDEO_2_PATH,
    'video_3': VIDEO_3_PATH,
    'video_4': VIDEO_4_PATH,
}

# Your videos will start appearing inside streamlit webapp 'Choose a video'.
```

- Click on `Detect Video Objects` button and the selected task (detection/segmentation) will start on the selected video.

### Detection on RTSP

- Select the RTSP stream button
- Enter the rtsp url inside the textbox and hit `Detect Objects` button

### Detection on YouTube Video URL

- Select the source as YouTube
- Copy paste the url inside the text box.
- The detection/segmentation task will start on the YouTube video url

To be uploaded..

## Acknowledgements

- This app is based on the YOLOv8(<https://github.com/ultralytics/ultralytics>) object detection algorithm.
- The app uses the Streamlit(<https://github.com/streamlit/streamlit>) library for the user interface.
- The original code is based in the source code from [CodingMantras/yolov8-streamlit-detection-tracking](https://github.com/CodingMantras/yolov8-streamlit-detection-tracking)
### Disclaimer

Please note that this project is intended for educational purposes only and should not be used in production environments yet.

**Hit star ⭐ if you like this repo!!!**
