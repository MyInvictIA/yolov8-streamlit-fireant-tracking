# 🌟 Real-time Object Detection and Tracking with YOLOv8 and Streamlit 🎉
Get ready for cutting-edge object detection magic! This web app combines the power of YOLOv8 for object detection and segmentation with the simplicity of the Streamlit framework to deliver real-time object detection and tracking in video streams. ✨

## 🚀 Demo WebApp
- (Coming soon!). Check out this app in action – it's up and running on the Streamlit cloud server! Thanks to the fantastic folks at Streamlit for supporting the community with cloud uploads. Here's where you can see it live:

- [yolov8-streamlit-detection-tracking-webapp]()

## 🕵️‍♀️ Tracking with Object Detection Demo Video
Coming soon! Stay tuned for a demo showcasing this awesome feature

## 📸 Demo Pics
-  Home page
- Picture coming soon!

## 📸 Page after uploading an image and object detection
Picture coming soon!

## 📸 Segmentation task on image
Picture coming soon!

## 📦 Requirements

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

## 🛠 Installation
- Clone this repo: `git clone https://github.com/MyInvictIA/yolov8-streamlit-fireant-tracking.git`
- Hop into the directory: `cd yolov8-streamlit-fireant-tracking`
- Upgrade PIP: `python -m pip install --upgrade pip`
- Follow the PyTorch installation instructions for your setup: https://pytorch.org/get-started/locally/

- For example, for a PC with Windows and NVIDIA GPU supporting CUDA 12.1:
```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## 🌟 Usage
Launch the app: `streamlit run app.py`
A new browser window will magically appear – that's where your image detection adventure begins!

### 🔧 ML Model Config
- Task time! Choose your mission: Segmentation
- Set your confidence level for the model
- Use the slider to adjust the confidence threshold (25-100).
- Once the model config is good to go, pick your source.

### 🖼 Image Detection
- The default image and its object-detected counterpart are proudly displayed on the main page.
- Choose your source (the "Image" radio button – ready for local uploads or internet images).
- Click "Browse files" to upload your image.
- Hit the "Detect Objects" button, and watch the object detection algorithm work its magic on your image with your chosen confidence threshold.
- The result – your image with detected objects – will appear. Click "Download Image" to save it!

## 🎬 Detection in Videos
- Demo Coming soon!.

- Press on `Detect Objects in Video ` button and the selected task will start on the selected video.

### 🌐 Detection on RTSP
- Select the RTSP stream button
- Enter the RTSP URL and press the "Detect Objects" button

### ▶️ Detection on YouTube Video URL
- Choose YouTube as your source
- Paste the URL into the text box.
- Let the detection/segmentation task do its thing on the YouTube video!

## 🙏 Acknowledgements

- This app owes its awesome object detection skills to the YOLOv8 algorithm (<https://github.com/ultralytics/ultralytics>).
- The Streamlit library (<https://github.com/streamlit/streamlit>) makes building the user interface a breeze.
- The original code is based in the source code from [CodingMantras/yolov8-streamlit-detection-tracking](https://github.com/CodingMantras/yolov8-streamlit-detection-tracking)

### ⚠️ Disclaimer
- This project is currently rockin' the educational world.  Hold tight before deploying it in production environments!
- If you love this repo, don't forget to leave a star! ⭐
