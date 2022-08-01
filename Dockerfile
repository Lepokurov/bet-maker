FROM python:3.10
WORKDIR /
COPY . /usr/app/
WORKDIR /usr/app/
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
