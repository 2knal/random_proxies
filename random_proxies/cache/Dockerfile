# For cache server setup

FROM python:3.6-alpine

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python", "-m", "random_proxies.cache.app"]