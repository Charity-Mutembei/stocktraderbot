FROM python:3.11.7

WORKDIR /lumiapp

COPY utils.py /lumiapp/
COPY docker-test.py /lumiapp/
COPY .env /lumiapp/
COPY requirements.txt /lumiapp/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "docker-test.py"]