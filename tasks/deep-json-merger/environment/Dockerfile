FROM ubuntu:22.04

# Install python3

RUN apt-get update && \

    apt-get install -y python3 && \

    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy python utility and JSON configuration files

COPY merge_configs.py defaults.json user_settings.json /app/

RUN mkdir -p /tmp

CMD ["python3", "/app/merge_configs.py"]
