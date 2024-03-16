import streamlit as st
import requests
import os
from pathlib import Path
import PIL

# Set page layout
st.set_page_config(
    page_title="Ant Detection using YOLOv8",
    page_icon="🐜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("Fire Ant Detection using YOLOv8")

# Sidebar
st.sidebar.header("Image Upload")

# File uploader in the sidebar
uploaded_image = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Detect Objects button in the sidebar
if st.sidebar.button('Detect Objects'):
    if uploaded_image is not None:
        # Display uploaded image
        st.subheader("Uploaded Image")
        st.image(uploaded_image, use_column_width=True)

        # Convert the uploaded image to bytes
        image_bytes = uploaded_image.getvalue()

        # Send the image to the API endpoint
        response = requests.post('http://backend:8000/detect', files={'image': image_bytes})

        if response.status_code == 200:
            result = response.json()
            detected_objects = result['detected_objects']
            original_filename = result['original_filename']
            processed_filename = result['processed_filename']

            # Display the processed image
            st.subheader("Processed Image")
            processed_image_path = f"/app/processed_images/{processed_filename}"
            if os.path.exists(processed_image_path):
                st.image(processed_image_path, use_column_width=True)
            else:
                st.warning("Processed image not found.")

            # Display the detected objects
            st.subheader("Detected Objects")
            if len(detected_objects) > 0:
                for obj in detected_objects:
                    st.write(f"- Class: {obj['class']}, Confidence: {obj['confidence']:.2f}")
            else:
                st.write("No objects detected.")
        else:
            st.error("Error occurred while detecting objects.")
    else:
        st.warning("Please upload an image.")

# Add a button in the sidebar for the "Library" section
if st.sidebar.button("Library"):
    # Create a section to display all processed images
    st.header("Processed Images")
    processed_images_dir = "/app/processed_images"
    original_images_dir = "/app/original_images"

    if os.path.exists(processed_images_dir) and os.path.exists(original_images_dir):
        processed_images = os.listdir(processed_images_dir)
        for image_file in processed_images:
            processed_image_path = os.path.join(processed_images_dir, image_file)
            original_image_path = os.path.join(original_images_dir, image_file.replace("_processed", "_original"))

            if os.path.exists(original_image_path):
                st.subheader(f"Image: {image_file}")
                col1, col2 = st.columns(2)
                with col1:
                    st.image(original_image_path, caption="Original Image", use_column_width=True)
                with col2:
                    st.image(processed_image_path, caption="Processed Image", use_column_width=True)
            else:
                st.warning(f"Original image not found for {image_file}")
    else:
        st.warning("No processed images found.")