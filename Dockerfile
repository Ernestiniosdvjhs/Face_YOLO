FROM python:3.9
#задает базовый образ
WORKDIR /usr/src/app/ 
#задаёт рабочую директорию 
COPY requirements.txt .
#копирует requirements.txt в директорию 
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y python3-opencv
RUN apt-get install -y ffmpeg
RUN pip install opencv-python
#скачивает все необходимые библиотеки
COPY . .
#копирует все в рабочую директорию
EXPOSE 8888
#указывает на необходимость открыть порт
CMD ["python", "app.py"]
#выполняет app.py
