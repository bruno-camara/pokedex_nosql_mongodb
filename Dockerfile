FROM python:3.10-alpine

WORKDIR /usr/app

COPY . .

RUN pip install pymongo 

CMD ["python3", "./main.py"]