# Dockerfile.multicast

FROM python:3.11-slim

# Install tcpdump so we can capture traffic inside any container
RUN apt-get update && \
    apt-get install -y --no-install-recommends tcpdump && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy multicast scripts into the image
COPY multicast_sender.py   .
COPY multicast_receiver.py .

# No additional pip packages needed – only stdlib is used
CMD ["python", "multicast_receiver.py"]