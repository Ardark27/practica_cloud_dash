FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .

EXPOSE 8080

CMD gunicorn -b 0.0.0.0:8080 pagina_dash:server