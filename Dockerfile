FROM python:3.10.4
COPY requirements.txt app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY app/. /app
CMD ["python3", "app.py"]