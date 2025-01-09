FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libtk8.6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./

CMD ["python", "app.py"]
