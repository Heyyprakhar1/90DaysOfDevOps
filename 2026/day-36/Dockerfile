FROM python:3.11-slim

RUN groupadd -r project && useradd -r -g project Prakhar

WORKDIR /app

COPY requirements.txt .

COPY . .

COPY app.py .

RUN pip install -r requirements.txt

RUN chown -R Prakhar:project /app

USER Prakhar

EXPOSE 5000

CMD ["python","app.py"]

