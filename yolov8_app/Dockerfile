# Dockerfile
# Use an official PyTorch CUDA runtime as a parent image
FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501
EXPOSE 8000

# Run app.py when the container launches
CMD uvicorn main:app --host 0.0.0.0 --port 8000 --reload & streamlit run --server.port 8501 app.py