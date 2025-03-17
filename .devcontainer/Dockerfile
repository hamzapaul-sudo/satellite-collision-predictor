# Use a base image with Python & Java
FROM mcr.microsoft.com/devcontainers/python:3.11

# Install OpenJDK (required for Orekit)
RUN apt-get update && apt-get install -y openjdk-17-jdk

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
