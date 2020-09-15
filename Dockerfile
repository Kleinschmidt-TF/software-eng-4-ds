FROM python:3.6

WORKDIR /code
ENV PATH=$PATH:/code
ENV PYTHONPATH /code
ENV MPLBACKEND agg

# install python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./run.py"]
