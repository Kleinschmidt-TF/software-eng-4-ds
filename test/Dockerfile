FROM python:3.6

WORKDIR /demand_forecast
ENV PATH=$PATH:/demand_forecast
ENV PYTHONPATH /demand_forecast
ENV MPLBACKEND agg

# install python requirements
COPY requirements.tests.txt ./
RUN pip install --no-cache-dir -r requirements.tests.txt

COPY . .
