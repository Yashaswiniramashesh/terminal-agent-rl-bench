FROM ubuntu:22.04

# Install python3
RUN apt-get update && \
    apt-get install -y python3 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy python utility and test markdown document
COPY extract_links.py document.md /app/

RUN mkdir -p /tmp

CMD ["python3", "/app/extract_links.py"]
