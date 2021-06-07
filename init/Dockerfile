FROM python:3.8-alpine
WORKDIR /code
COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/
CMD ["init.py"]
ENTRYPOINT ["python3"]
