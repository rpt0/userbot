FROM python:3.10-slim

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    ffmpeg git neofetch apt-utils libmediainfo0v5 sqlite3 \
    libgl1-mesa-glx libglib2.0-0 libxml2-dev libxslt-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY req.txt .

RUN pip3 install -U pip && \
    pip3 install --no-cache-dir -r req.txt

COPY . .
COPY start.sh .

RUN chmod +x start.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 7860-8000

ENTRYPOINT ["./start.sh"]