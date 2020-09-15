
FROM python:3.6-alpine

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONPATH "${PYTHONPATH}:/app"

EXPOSE 5000

RUN mkdir /app

COPY . /app

RUN pip install -r ./app/requirements.txt

CMD  ["python3", "./app/app.py"]