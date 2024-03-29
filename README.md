# 🌟🐜 Real-time Fire Ants and Nests Detection and Tracking with YOLOv8 and Streamlit 🎉👀
Get ready for cutting-edge object detection magic! This web app combines the power of YOLOv8 🔍 for object detection and segmentation with the simplicity of the Streamlit framework to deliver real-time object detection and tracking in video streams. ✨🎥

## 📝⌛ To Do
- [ ] Examples of the app running.
- [ ] Examples of API usage.
- [ ] 🔄 Migrate the application to a new Dashboard based on Vue.js and Flask among others.

## 🚀💻 Demo WebApp
[![Demonstration of WebApp](https://img.youtube.com/vi/mBqrbDk6U6c/0.jpg)](https://www.youtube.com/watch?v=mBqrbDk6U6c)

- Check out this app in action 🏃‍♂️ – it's up and running on the Streamlit cloud server! ☁️ Thanks to the fantastic folks at Streamlit for supporting the community with cloud uploads. Here's where you can see it live:

- [yolov8-streamlit-detection-tracking-webapp]()

## 🕵️‍♀️🔎 Tracking with Object Detection Demo Video
Coming soon! 📹 Stay tuned for a demo showcasing this awesome feature

## 📸📷 Demo Pics
- Home page 🏠
- Picture coming soon!  📸

## 📸🔍 Page after uploading an image and object detection
Picture coming soon! 📷

## 📸↔️ Segmentation task on image
Picture coming soon! 🎞️

## 📦🔨 Requirements

* requests
* streamlit
* pathlib
* pandas
* Pillow
* numpy
* opencv-python-headless
* lapx
* Cython
* Pillow
* ultralytics
* python-multipart
* aiofiles
* datetime
* pytube

## 🛠🔧 Installation
- Clone this repo: `git clone https://github.com/MyInvictIA/yolov8-streamlit-fireant-tracking.git`
- Hop into the directory: `cd yolov8-streamlit-fireant-tracking`
- Run the following command tu build the docker container: `docker-compose build`
- Run the following command tu run the docker container: `docker-compose up -d`

- yolov8_app can run on NVIDIA GPU thanks to CUDA and on CPU if you don't have a GPU.

## 🌟🔭 Usage
* Launch the app: `docker-compose up -d`
* Open a browser and get into the following URL: `http://localhost:8501`

### 🔧🧰 ML Model Config
- Task time! Choose your mission: 🎯 Segmentation* supported only.
- Set your confidence level for the model, using the slider to adjust the confidence threshold (25-100).
- Once the model config is good to go, pick your source.

### 🖼🔍 Image Detection
- The default image and its object-detected counterpart are proudly displayed on the main page.
- Choose your source (the "Image" radio button – ready for local uploads or internet images).
- Click "Browse files" to upload your image.
- Hit the "Detect Objects" button, and watch the object detection algorithm work its magic on your image with your chosen confidence threshold.
- The result – your image with detected objects – will appear. Click "Download Image" to save it!

## 🎬🔎 Detection in Videos
- Demo Coming soon!.

- Press on `Detect Objects in Video ` button and the selected task will start on the selected video.

### 🌐🔍 Detection on RTSP
- Select the RTSP stream button
- Enter the RTSP URL and press the "Detect Objects" button

### ▶️🔮 Detection on YouTube Video URL
- Choose YouTube as your source
- Paste the URL into the text box.
- Let the detection/segmentation task do its thing on the YouTube video!

## 🙏☺️ Acknowledgements

- This app owes its awesome object detection skills to the YOLOv8 algorithm (<https://github.com/ultralytics/ultralytics>).
- The Streamlit library (<https://github.com/streamlit/streamlit>) makes building the user interface a breeze.
- The original code is based in the source code from [CodingMantras/yolov8-streamlit-detection-tracking](https://github.com/CodingMantras/yolov8-streamlit-detection-tracking)

## ⚠️😅 Disclaimer
- This project is currently rockin' the educational world.  Hold tight before deploying it in production environments! 🚀
- If you love this repo, don't forget to leave a star! ⭐

## 🏆🌐 Contests and Competitions
This project has taken part in the following contests and competitions:
- [Castilla y León's Boards Innovation Contest 2023](https://www.tramitacastillayleon.jcyl.es/web/jcyl/AdministracionElectronica/es/Plantilla100Detalle/1251181050732/Premio/1285312846458/Propuesta)
- [Huawei ICT Competition in the Innovate Stage 2023-24.](https://e.huawei.com/en/talent/#/ict/innovation-details?zoneCode=071217&zoneId=98269613&compId=85131995&divisionName=Europe&type=C002&isCollectGender=N&enrollmentDeadline=null&compTotalApplicantCount=39)
![huawei_ict_competition_2023-24.jpg](assets%2Fhuawei_ict_competition_2023-24.jpg)