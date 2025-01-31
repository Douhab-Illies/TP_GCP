FROM python:3.10-slim

COPY . /opt/app
WORKDIR /opt/app

RUN pip install --no-cache-dir -r requirements.txt

ENV BUCKET=$BUCKET

EXPOSE 8080
CMD ["python", "/opt/app/app_cloud.py"]
