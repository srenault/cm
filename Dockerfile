FROM python:3.7-alpine

WORKDIR /app

COPY . .

RUN python setup.py install

WORKDIR /app/tools

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
