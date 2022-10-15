FROM python:3.10.4
WORKDIR /app
COPY app/ /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python3", "app.py"]