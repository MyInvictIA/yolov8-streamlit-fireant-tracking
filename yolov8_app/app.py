# Python In-built packages
from pathlib import Path
import PIL

# External packages
import streamlit as st
import pandas as pd
import requests
import base64

# Local Modules
import settings
import helper

# Setting page layout
st.set_page_config(
    page_title="Ant Detection using YOLOv8",
    page_icon="🐜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("Fire Ant Detection using YOLOv8")

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
                source_img = PIL.Image.open(response.raw)
            except Exception as ex:
                st.error("Error occurred while opening the image from URL.")
                st.error(ex)

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = PIL.Image.open(default_image_path)
                st.image(default_image_path, caption="Default Image",
                         use_column_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image",
                         use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='Detected Image',
                     use_column_width=True)
        else:
            if st.sidebar.button('Detect Objects'):
                res = model.predict(uploaded_image, conf=confidence)
                boxes = res[0].boxes
                ant_count = 0
                anthill_count = 0

                # Count ants and anthills
                for box in boxes:
                    if box.cls == settings.ANT_CLASS_INDEX:
                        ant_count += 1
                    elif box.cls == settings.ANTHILL_CLASS_INDEX:
                        anthill_count += 1

                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Detected Image',
                         use_column_width=True)

                # Create a container for the distribution table
                distribution_container = st.container()

                try:
                    with st.expander("Detection Results"):
                        for box in boxes:
                            st.write(box.data)

                    # Create a list of dictionaries
                    items = []
                    for category, count in zip(['Ant Hill', 'Ants'], [anthill_count, ant_count]):
                        items.append({'Category': category, 'Amount': count})

                    # Create a DataFrame from the list
                    df = pd.DataFrame(items)

                    # Show the table
                    with distribution_container:
                        st.markdown('#### Distribution of Identified Objects')
                        st.dataframe(df)

                except Exception as ex:
                    # st.write(ex)
                    st.write("No image is uploaded yet!")

elif source_radio == settings.VIDEO:
    #helper.play_stored_video(confidence, model)
    video_file = st.sidebar.file_uploader("Choose a video...", type=["mp4", "avi", "mov", "mkv"])
    if video_file is not None:
        video_bytes = video_file.read()

        if st.sidebar.button('Detect Objects'):
            try:
                anthill_count, ant_count = helper.process_video(video_bytes, confidence, model)

                # Create a DataFrame with the detection results
                data = {
                    'Category': ['Anthill', 'Ants'],
                    'Amount': [anthill_count, ant_count]
                }
                df = pd.DataFrame(data)

                # Display the DataFrame
                st.dataframe(df)

                # Add a download button for the DataFrame
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="detection_results.csv">Download CSV</a>'
                st.markdown(href, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error processing video: {str(e)}")
    else:
        st.warning("Please upload a video file.")

elif source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model)

elif source_radio == settings.RTSP:
    helper.play_rtsp_stream(confidence, model)

elif source_radio == settings.YOUTUBE:
    helper.play_youtube_video(confidence, model)

else:
    st.error("Please select a valid source type!")
