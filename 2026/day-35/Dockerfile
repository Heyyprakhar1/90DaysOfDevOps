FROM python:3.9-slim

RUN groupadd -r DevOps && useradd -r -g DevOps Prakhar

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN chown -R Prakhar:DevOps /app

USER Prakhar

EXPOSE 5000

CMD ["python","app.py"]
