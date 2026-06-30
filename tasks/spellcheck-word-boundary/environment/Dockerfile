FROM ubuntu:22.04

# Install python3
RUN apt-get update && \
    apt-get install -y python3 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy python utility and text draft
COPY spellcheck.py draft.txt /app/

RUN mkdir -p /tmp

CMD ["python3", "/app/spellcheck.py"]
