FROM python:3

RUN apt clean
RUN apt update --fix-missing
RUN apt install -y postgresql  # зачем тут ставить postgresql?
RUN apt postgresql-contrib
RUN apt libpq-dev
RUN apt python3-dev

RUN pip install --upgrade pip

COPY ./webnotes/ ./
#RUN pip freeze > requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY wait-for-postgres.sh .
RUN chmod +x wait-for-postgres.sh

RUN pip3 install gunicorn
