FROM python:3.6.9

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install -r ./requirements.txt

COPY ./src/ /app/

CMD [ "python", "server.py" ]