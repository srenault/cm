FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN python setup.py install

WORKDIR /usr/src/app/tools

RUN pip install -r requirements.txt

RUN pip install -e ../

ENTRYPOINT [ "python" ]
