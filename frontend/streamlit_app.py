import streamlit as st
import requests
import os
import pandas as pd
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Ant Detection using YOLOv8",
    page_icon="🐜",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Título principal de la página
st.title("Fire Ant Detection in Real-Time using YOLOv8 - v0.3")

# Barra lateral
st.sidebar.header("Source")

# Opciones de origen
source_option = st.sidebar.radio("Choose the Source", ["Image", "Video"], label_visibility='collapsed')

if source_option == "Image":
    # Barra lateral
    st.sidebar.header("Image Config")
    image_option = st.sidebar.radio("Choose Image Source", ["Local", "URL"], label_visibility='collapsed')

    if image_option == "Local":
        image_file = st.sidebar.file_uploader("Choose an image...",
                                              type=("jpg", "jpeg", "png", 'bmp', 'webp', 'tiff', 'gif'))
        image_data = image_file.read() if image_file is not None else None
    elif image_option == "URL":
        image_url = st.sidebar.text_input("Enter Image URL")
        image_data = requests.get(image_url).content if image_url else None

    # Crear el espacio de 2 columnas
    col1, col2 = st.columns(2)

    # Si la imagen está seleccionada
    if image_file is not None:
        uploaded_image = Image.open(image_file)
        col1.image(uploaded_image, caption=f'Uploaded Image: {image_file.name}', use_column_width=True)

        if col1.button('Process Image', help="Click to detect ants on the image"):
            response = requests.post("http://backend:8000/detect_img", files={"image": image_data})
            if response.status_code == 200:
                result = response.json()
                detected_objects = result['detected_objects']
                processed_filename = result['processed_filename']

                processed_image_path = f"/app/processed_images/{processed_filename}"
                if os.path.exists(processed_image_path):
                    processed_image = Image.open(processed_image_path)
                    col2.image(processed_image, caption="Processed Image", use_column_width=True)
                else:
                    st.warning("Processed image not found.")

                if len(detected_objects) > 0:
                    # Mostrar número de detecciones
                    col2.write(f"Number of Detections: {len(detected_objects)}")

                    # Mostrar tabla con las detecciones
                    df = pd.DataFrame(detected_objects)
                    # Make the DataFrame index start from 1
                    df.index = df.index + 1
                    df.to_csv(f"/app/processed_images/{processed_filename.replace('.jpg', '_detections.csv')}",
                              index=True)
                    col2.dataframe(df)

                else:
                    st.write("No objects detected.")
    elif image_option == "URL":
        pass

elif source_option == "Video":
    st.sidebar.header("Video Config")
video_file = st.sidebar.file_uploader("Choose a video...", type=["mp4", "avi", "mov", "mkv"])
if video_file is not None:
    video_data = video_file.read()
    response = requests.post("http://backend:8000/detect_video", files={"video": video_data})
    if response.status_code == 200:
        result = response.json()
        detected_objects = result['detected_objects']
        original_filename = result['original_filename']
        processed_video_url = result['processed_video_url']  # Nueva línea de código

        # Display the detected objects
        st.subheader("Detected Objects")
        if len(detected_objects) > 0:
            df = pd.DataFrame(detected_objects)
            st.dataframe(df)
            # Make the DataFrame index start from 1
            df.index = df.index + 1
            # Display number of detections
            st.write(f"Number of Detections: {len(detected_objects)}")
        else:
            st.write("No objects detected.")

        # Display processed video
        st.subheader("Processed Video")
        st.video(processed_video_url)  # Nueva línea de código

    else:
        st.error("Error occurred while processing the video.")
else:
    st.warning("Please upload a video file.")

# Sección "Library"
if st.sidebar.button("See Processed Images Library"):
    st.header("Processed Images")
    processed_images_dir = "/app/processed_images"

    # Ordena los archivos por última hora de modificación (es decir, desde el más reciente al más antiguo)
    processed_images = sorted(os.listdir(processed_images_dir),
                              key=lambda x: os.path.getmtime(os.path.join(processed_images_dir, x)), reverse=True)

    if processed_images:
        for image_file in processed_images:
            # Cada entrada de la biblioteca es un bloque de columna
            col1, col2 = st.columns(2)
            processed_image_path = os.path.join(processed_images_dir, image_file)
            if image_file.endswith('_detections.csv'):
                df_detections = pd.read_csv(processed_image_path)
                col2.write(f"Number of Detections: {len(df_detections)}")
                col2.dataframe(df_detections)
            elif image_file.endswith(('.jpg', '.jpeg', '.png', 'bmp', 'webp', 'tiff', 'gif')):
                processed_image = Image.open(processed_image_path)
                col1.image(processed_image, caption="Processed Image", use_column_width=True)
    else:
        st.warning("No processed images found.")