# Use Python as the base image
FROM python:3.11

# Install dependencies for Orekit
RUN apt-get update && apt-get install -y openjdk-17-jdk

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose FastAPI & Streamlit ports
EXPOSE 8000 8501

# Start FastAPI & Streamlit together
CMD ["sh", "-c", "streamlit run app.py --server.port 8501 --server.address 0.0.0.0"]
