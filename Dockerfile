# Dockerfile
FROM python:3.8-slim

WORKDIR /usr/src/app

COPY mi_script_tercerentrega.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./mi_script_tercerentrega.py"]
