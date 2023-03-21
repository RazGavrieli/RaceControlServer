FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5672

COPY launch_sensors.sh .
COPY gpsModule.py .
COPY timingModule.py .

CMD ["./launch_sensors.sh", "f"]
