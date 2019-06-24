FROM python:3.7.2-alpine3.8

RUN apk update && apk upgrade && apk add bash
COPY . ./app

EXPOSE 80
WORKDIR ./app

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN pip install --upgrade -r requirements.txt

CMD ["python3", "./main.py"]