# Python In-built packages
from pathlib import Path
from PIL import Image
from urllib.parse import urlparse

# External packages
import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import os

# Local Modules
import settings
import helper
from helper import process_video


# Setting page layout
st.set_page_config(
    page_title="Fire Ant Detection App",
    page_icon="🐜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("Demo: Fire Ant Detection using YOLOv8")

# Sidebar
st.sidebar.header("ML Model Config")

# Model Options
model_type = st.sidebar.radio(
    "Select Task", ['Segmentation'])

confidence = float(st.sidebar.slider(
    "Select Model Confidence", 25, 100, 40)) / 100

# Selecting Detection Or Segmentation
if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)
elif model_type == 'Segmentation':
    # Change the model to use in settings.py
    model_path = Path(settings.SEGMENTATION_MODEL)

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST)

source_img = None

# If image is selected
if source_radio == settings.IMAGE:
    source_option = st.sidebar.radio("Image Source", ["Local", "URL"])
    if source_option == "Local":
        source_img = st.sidebar.file_uploader(
            "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp', 'tiff', 'gif'))
    elif source_option == "URL":
        url = st.sidebar.text_input("Enter Image URL")
        if url:
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()
                source_img = BytesIO(response.content)
            except Exception as ex:
                st.error("Error occurred while opening the image from URL.")
                st.error(ex)

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = Image.open(default_image_path)
                st.image(default_image_path, caption="Default Image",
                         use_column_width="auto")
            else:
                uploaded_image = Image.open(source_img)
                st.image(source_img, caption="Uploaded Image",
                         use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='Detected Image',
                     use_column_width="auto")
        else:
            if st.sidebar.button('Run Detection'):
                res = model.predict(uploaded_image, conf=confidence)
                boxes = res[0].boxes

                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Detected Image',
                         use_column_width=True)

                # Check for any detection before processing the result.
                if boxes:
                    # Process result tensor
                    class_mapping = {
                        0: 'Barbary_Harvester_Ant',
                        1: 'Fire_Ant_Nest',
                        2: 'Mediterranean_Acrobat_Ant',
                        3: 'Mediterranean_Acrobat_Nest',
                        4: 'Red_Imported_Fire_Ant',
                        # Add more mappings as necessary
                    }
                    # Extract information from the classes
                    classes = [class_mapping[int(box.data[0][5].item())] for box in boxes]
                    # Counting the occurrences of each class
                    class_counts = {i: classes.count(i) for i in classes}
                    df = pd.DataFrame(list(class_counts.items()), columns=['Class', 'Count'])

                    # Create a container for the distribution table
                    distribution_container = st.container()

                    with distribution_container:
                        st.dataframe(df)

                    try:
                        with st.expander("Detection Results"):
                            for box in boxes:
                                st.write(box.data)
                    except Exception as ex:
                        st.write("No image is uploaded yet!")

                else:
                    st.write("No objects were detected in the image.")

# If image with API is selected
if source_radio == settings.IMAGE_API:
    source_option = st.sidebar.radio("Image Source", ["Local", "URL"])
    if source_option == "Local":
        source_img = st.sidebar.file_uploader(
            "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp', 'tiff', 'gif'))
    elif source_option == "URL":
        url = st.sidebar.text_input("Enter Image URL")
        if url:
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()
                source_img = BytesIO(response.content)
            except Exception as ex:
                st.error("Error occurred while opening the image from URL.")
                st.error(ex)

    df = pd.DataFrame()  # Inicializar df como un DataFrame vacío
    col1, col2 = st.columns(2)
    st.write("API Image Detection doesn't work in Streamlit Servers becase the API can't load there. Please run this locally to test it out.")
    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = Image.open(default_image_path)
                st.image(default_image_path, caption="Default Image",
                         use_column_width="auto")
            else:
                uploaded_image = Image.open(source_img)
                st.image(source_img, caption="Uploaded Image via **API**",
                         use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='Detected Image',
                     use_column_width="auto")
        else:
            if st.sidebar.button('Run Detection'):
                # source_img contents are sent as a POST request to the API
                api_url = 'http://localhost:8000/detect_img'  # replace with your API URL
                files = {'image': source_img}
                #response = requests.post(api_url, files=files)
                filename = os.path.basename(urlparse(url).path) if urlparse(url).path else f"default_image_{now}"
                response = requests.post(api_url, files={'image': source_img}, data={'filename': filename})
                response.raise_for_status()  # make sure we get a 200 OK response
                api_response = response.json()

                # You can display the processed image
                processed_image_filename = api_response['processed_filename']
                processed_image_path = os.path.join('./images/processed',
                                                    processed_image_filename)  # specify the correct path
                st.image(processed_image_path, use_column_width=True, caption='Processed image via **API**')

                # Finally, use the api_response here
                detected_objects = api_response['detected_objects']
                df = pd.DataFrame(detected_objects)

                # Ensure the DataFrame is not empty before accessing its 'class' field
                if not df.empty:  # Asegurarse de que el DataFrame no esté vacío
                    st.dataframe(df)
                    # Count the occurrence of each class
                    class_counts = df['class'].value_counts()

                    # Calculate total occurrence
                    total_count = class_counts.sum()

                    # Convert to DataFrame
                    count_df = class_counts.reset_index().rename(columns={'index': 'class', 'class': 'total'})

                    # Use concat instead of append
                    count_df = pd.concat([count_df], ignore_index=True)
                    # Display the count DataFrame
                    st.markdown("## Summary")
                    st.table(count_df)
                else:
                    st.write("No objects were detected in the image.")






elif source_radio == settings.VIDEO:
    video_file = st.sidebar.file_uploader("Choose a video...", type=["mp4", "avi", "mov", "mkv"])
    if video_file is not None:
        video_bytes = video_file.read()

        if st.sidebar.button('Run Detection'):
            try:
                classes_detected = process_video(video_bytes, confidence, model)

                ## Warning: Couting is not working for videos!!
                # Use the same class mapping as in the image example
                class_mapping = {
                    0: 'Barbary_Harvester_Ant',
                    1: 'Fire_Ant_Nest',
                    2: 'Mediterranean_Acrobat_Ant',
                    3: 'Mediterranean_Acrobat_Nest',
                    4: 'Red_Imported_Fire_Ant',
                    # Add more mappings as necessary
                }

                # Translate class IDs to class names
                translated_classes = [class_mapping[c] for c in classes_detected]
                class_counts = {i: translated_classes.count(i) for i in translated_classes}
                df = pd.DataFrame(list(class_counts.items()), columns=['Class', 'Count'])

                # Display the DataFrame
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error processing video: {str(e)}")
    else:
        st.warning("Please upload a video file.")

# Not working yet in Docker
elif source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model)
# Haven't tested this yet
elif source_radio == settings.RTSP:
    helper.play_rtsp_stream(confidence, model)

elif source_radio == settings.YOUTUBE:
    helper.play_youtube_video(confidence, model)

# else:
#     st.warning("Please select a valid source type!")
