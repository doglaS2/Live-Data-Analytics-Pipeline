FROM python:3.9-slima

COPY app.py .

CMD FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]["python", "app.py"]