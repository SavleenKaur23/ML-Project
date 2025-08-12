FROM python:3.10-slim-buster  # BaseImage
WORKDIR /app  # folder will get created in Docker
COPY . /app  #copy the entire project in app folder

RUN apt update -y && apt install awscli - y

RUN pip install -r requirements.txt

CMD ["python3", "application.py"]