# Use the official Python image from Docker Hub
FROM python:3.11.5

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --default-timeout=1000 --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app's source code to the container
COPY . .

# Expose the ports for FastAPI:8000 and Streamlit:8501
EXPOSE 8000
EXPOSE 8501

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Command to start Streamlit first, then FastAPI
CMD ["sh", "-c", "streamlit run stream.py --server.port 8501 --server.address 0.0.0.0 & sleep 5 && uvicorn app:app --host 0.0.0.0 --port 8000"]
