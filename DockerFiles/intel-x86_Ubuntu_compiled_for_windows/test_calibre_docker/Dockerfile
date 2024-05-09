# Use the latest Ubuntu base image
FROM ubuntu:latest

# Set non-interactive installation mode
ENV DEBIAN_FRONTEND=noninteractive

# Update packages and install necessary libraries
RUN apt-get update && \
    apt-get install -y wget xz-utils libxcb-cursor0 python3 python3-pip \
    libegl1 libopengl0 && \
    wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sh /dev/stdin

# Set the environment path to include Calibre
ENV PATH="/opt/calibre:$PATH"

COPY w.txt /home/w.txt

# Copy your Python script that tests Calibre's functionality
COPY calibre_test.py /home/calibre_test.py

RUN python3 /home/calibre_test.py

# Run the Python script to test Calibre
CMD ["python3", "/home/calibre_test.py"]
